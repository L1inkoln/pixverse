from fastapi import APIRouter, Depends, File, Form, UploadFile
from app.schemas.get_status_schema import GetStatusRequest, GetStatusResponse
from app.schemas.text2video_schema import Text2VideoRequest, Text2VideoResponse
from app.schemas.image2video_schema import Image2VideoResponse
from app.services.pixverse_client import (
    image_to_video,
    text_to_video,
    get_generation_status,
)
from app.models.db import get_async_session, save_generation_task

router = APIRouter(prefix="", tags=["PixverseMethods"])


@router.post("/text2video", response_model=Text2VideoResponse)
async def generate_video_from_text(
    request: Text2VideoRequest, session=Depends(get_async_session)
):
    """
    Этот endpoint обрабатывает запрос на генерацию видео из текста.

    Параметры:
    - app_bundle_id: Идентификатор пакета приложения.
    - apphud_user_id: Идентификатор пользователя Apphud.
    - prompt: Подсказка для генерации видео.

    Возвращает:
    - Ответ модели Text2VideoResponse с идентификатором видео или сообщением об ошибке.
    """
    await save_generation_task(
        session=session,
        request_type="text",
        app_bundle_id=request.app_bundle_id,
        apphud_user_id=request.apphud_user_id,
        prompt=request.prompt,
    )
    return await text_to_video(request.prompt)


@router.post("/image2video", response_model=Image2VideoResponse)
async def generate_video_from_image(
    app_bundle_id: str = Form(..., description="App Bundle ID"),
    apphud_user_id: str = Form(..., description="Apphud User ID"),
    prompt: str = Form(...),
    image: UploadFile = File(...),
    session=Depends(get_async_session),
):
    """
    Этот endpoint обрабатывает запрос на генерацию видео из изображения.

    Параметры:
    - app_bundle_id: Идентификатор пакета приложения.
    - apphud_user_id: Идентификатор пользователя Apphud.
    - prompt: Подсказка для генерации видео.
    - image: Загружаемое изображение в формате файла.

    Возвращает:
    - Ответ модели Image2VideoResponse с идентификатором видео или сообщением об ошибке.
    """
    await save_generation_task(
        session=session,
        request_type="img",
        app_bundle_id=app_bundle_id,
        apphud_user_id=apphud_user_id,
        prompt=prompt,
    )
    return await image_to_video(image, prompt)


@router.post("/get-status", response_model=GetStatusResponse)
async def get_generate_status(request: GetStatusRequest):
    """
    Этот endpoint возвращает состояние генерации и ссылку если видео сгенерировалось.

    Параметры:
    - app_bundle_id: Идентификатор пакета приложения.
    - apphud_user_id: Идентификатор пользователя Apphud.
    - video_id: Идентификатор задачи видеогенерации.

    Возвращает:
    - Ответ со статусом видеогенерации.
    - Ссылку если готово видео.
    """
    return await get_generation_status(request.video_id)
