from pydantic import BaseModel, Field, HttpUrl
from typing import List


class SelectedVideo(BaseModel):
    url: HttpUrl


class SelectedVideosPayload(BaseModel):
    videos: List[SelectedVideo] = Field(min_length=1, max_length=50)
