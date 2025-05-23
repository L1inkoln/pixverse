import uuid
from fastapi import HTTPException
import httpx
from dotenv import load_dotenv
import oss2
from app.exceptions import raise_for_pixverse_error
from app.schemas.get_status_schema import GetStatusResponse
from app.schemas.image2video_schema import Image2VideoResponse
from app.utils import (
    build_image2video_payload,
    build_text2video_payload,
    get_pixverse_headers,
    get_status_generate_payload,
)
from app.schemas.text2video_schema import Text2VideoResponse

load_dotenv()

headers = get_pixverse_headers()

# TODO вынести в конфиг
PIXVERSE_TEXT2VIDEO_URL = "https://app-api.pixverse.ai/creative_platform/video/t2v"
PIXVERSE_IMAGE2VIDEO_URL = "https://app-api.pixverse.ai/creative_platform/video/i2v"
PIXVERSE_STATUS_URL = (
    "https://app-api.pixverse.ai/creative_platform/video/list/personal"
)
PIXVERSE_UPLOAD_URL = (
    "https://app-api.pixverse.ai/creative_platform/media/batch_upload_media"
)
UPLOAD_TOKEN_URL = "https://app-api.pixverse.ai/creative_platform/getUploadToken"


async def text_to_video(prompt: str) -> Text2VideoResponse:
    payload = build_text2video_payload(prompt)
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                PIXVERSE_TEXT2VIDEO_URL, headers=headers, json=payload
            )
            data = response.json()

            if response.status_code == 200:
                if data.get("ErrCode") == 0:
                    video_id = data["Resp"].get("video_id")
                    return Text2VideoResponse(
                        video_id=str(video_id) if video_id else None
                    )
                else:
                    raise_for_pixverse_error(data.get("ErrCode"), data.get("ErrMsg"))

            raise HTTPException(status_code=response.status_code, detail=response.text)

    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Pixverse HTTP error: {str(e)}")


async def get_upload_token() -> dict:
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                UPLOAD_TOKEN_URL,
                headers=headers,
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to get upload token",
                )
            data = response.json()
            return data.get("Resp", {})
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=502, detail=f"Pixverse HTTP error (upload token): {str(e)}"
        )


async def upload_image_oss(
    image_bytes: bytes, filename: str, ak: str, sk: str, security_token: str
) -> bool:
    try:
        auth = oss2.StsAuth(ak, sk, security_token)
        bucket = oss2.Bucket(
            auth, "https://oss-accelerate.aliyuncs.com", "pixverse-fe-upload"
        )
        result = bucket.put_object(f"upload/{filename}", image_bytes)
        return result.status == 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OSS upload error: {str(e)}")


async def register_uploaded_file(filename: str, size: int) -> bool:
    payload = {
        "images": [{"name": filename, "size": size, "path": f"upload/{filename}"}]
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                PIXVERSE_UPLOAD_URL,
                headers=headers,
                json=payload,
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code, detail="Failed to register image"
                )
            return True
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=502, detail=f"Pixverse HTTP error (register file): {str(e)}"
        )


async def image_to_video(image, prompt: str) -> Image2VideoResponse:
    try:
        upload_data = await get_upload_token()
        ak = upload_data.get("Ak")
        sk = upload_data.get("Sk")
        security_token = upload_data.get("Token")
        if not (ak and sk and security_token):
            raise HTTPException(status_code=400, detail="Missing OSS credentials")

        image_bytes = await image.read()
        filename = f"{uuid.uuid4()}.jpg"

        await upload_image_oss(image_bytes, filename, ak, sk, security_token)
        await register_uploaded_file(filename, size=len(image_bytes))

        payload = build_image2video_payload(prompt, filename)
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                PIXVERSE_IMAGE2VIDEO_URL,
                headers=headers,
                json=payload,
            )
            data = response.json()

            if response.status_code == 200:
                if data.get("ErrCode") == 0:
                    return Image2VideoResponse(video_id=str(data["Resp"]["video_id"]))
                else:
                    raise_for_pixverse_error(data.get("ErrCode"), data.get("ErrMsg"))

            raise HTTPException(status_code=response.status_code, detail=response.text)

    except HTTPException:
        raise  # пропускаем уже обработанные ошибки
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


async def get_generation_status(video_id: str) -> GetStatusResponse:
    headers = get_pixverse_headers()
    payload = get_status_generate_payload()
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(
                PIXVERSE_STATUS_URL, headers=headers, json=payload
            )
            data = response.json()

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to get video status",
                )

            videos = data.get("Resp", {}).get("data", [])
            for video in videos:
                if str(video.get("video_id")) == video_id:
                    status_code = video.get("video_status")
                    video_url = video.get("url")
                    first_frame = video.get("first_frame")

                    if status_code == 1 and first_frame:
                        return GetStatusResponse(status="success", video_url=video_url)
                    elif status_code == 10:
                        return GetStatusResponse(status="generating")
                    else:
                        return GetStatusResponse(status="error")

            return GetStatusResponse(status="error")

    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=502, detail=f"Pixverse HTTP error (status): {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
