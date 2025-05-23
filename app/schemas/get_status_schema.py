from typing import Literal, Optional
from pydantic import BaseModel, Field


class GetStatusRequest(BaseModel):
    app_bundle_id: str = Field(..., description="App Bundle ID")
    apphud_user_id: str = Field(..., description="Apphud User ID")
    video_id: str = Field(..., description="Video generation ID")


class GetStatusResponse(BaseModel):
    status: Literal["generating", "error", "success"]
    video_url: Optional[str] = None
