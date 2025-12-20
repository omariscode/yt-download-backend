from pydantic import BaseModel
from typing import List

class SelectedVideo(BaseModel):
    url: str
    select: bool

class SelectedVideosPayload(BaseModel):
    videos: List[SelectedVideo]
