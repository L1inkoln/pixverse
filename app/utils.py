import os
from dotenv import load_dotenv

load_dotenv()

PIXVERSE_TOKEN = os.getenv("PIXVERSE_TOKEN")


def get_pixverse_headers() -> dict:
    return {
        "accept": "application/json, text/plain, */*",
        "x-platform": "Web",
        "token": PIXVERSE_TOKEN,
        "content-type": "application/json",
    }


def build_text2video_payload(prompt: str) -> dict:
    return {
        "prompt": prompt,
        "duration": 5,  # Длительность: 5 или 8 секунд
        "quality": "360p",  # Качество: 360p, 540p, 720p, 1080p
        "aspect_ratio": "16:9",  # Соотношение: 16:9, 4:3, 1:1, 3:4, 9:16
        "motion_mode": "normal",
        "model": "v4.5",
        "lip_sync_tts_speaker_id": "Auto",
    }


def build_image2video_payload(prompt: str, filename: str) -> dict:
    return {
        "customer_img_path": f"upload/{filename}",
        "prompt": prompt,
        "duration": 5,  # Длительность: 5 или 8 секунд
        "quality": "360p",  # Качество: 360p, 540p, 720p, 1080p
        "motion_mode": "normal",
        "model": "v4.5",
        "customer_img_url": f"https://media.pixverse.ai/upload/{filename}",
        "lip_sync_tts_speaker_id": "Auto",
    }


def get_status_generate_payload() -> dict:
    return {
        "offset": 0,
        "limit": 50,
        "filter": {"off_peak": 0},
        "web_offset": 0,
        "app_offset": 0,
    }
