from typing import Optional
from pydantic import BaseModel, Field


class Text2VideoRequest(BaseModel):
    app_bundle_id: str = Field(..., description="App Bundle ID")
    apphud_user_id: str = Field(..., description="Apphud User ID")
    prompt: str = Field(..., description="Text prompt for video generation")


class Text2VideoResponse(BaseModel):
    video_id: Optional[str] = Field(default=None, description="Generated video ID")
    message: Optional[str] = Field(default=None, description="Error message")
