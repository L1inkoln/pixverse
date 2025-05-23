from typing import Optional
from pydantic import BaseModel


class Image2VideoResponse(BaseModel):
    video_id: Optional[str] = None
    message: Optional[str] = None
