from pydantic import BaseModel, Field, HttpUrl
from typing import List


class SelectedVideo(BaseModel):
    url: HttpUrl


class SelectedVideosPayload(BaseModel):
    videos: List[SelectedVideo] = Field(ge=1, le=50)
