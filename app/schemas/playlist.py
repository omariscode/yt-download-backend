from pydantic import BaseModel
from typing import List

class Videos(BaseModel):
    id: str
    title: str
    duration: int

class Playlist(BaseModel):
    title: str
    count_videos: int
    videos: List[Videos]

class PlaylistCreate(BaseModel):
    url: str