from pydantic import BaseModel
from typing import List


class Videos(BaseModel):
    id: str
    title: str
    duration: int
    url: str
    thumbnail: str | None = None


class Playlist(BaseModel):
    title: str
    count_videos: int
    thumbnail: str | None
    videos: List[Videos]


class PlaylistCreate(BaseModel):
    url: str
