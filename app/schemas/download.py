from pydantic import BaseModel
from typing import List

class SelectedVideo(BaseModel):
    url: str

class SelectedVideosPayload(BaseModel):
    videos: List[SelectedVideo]
