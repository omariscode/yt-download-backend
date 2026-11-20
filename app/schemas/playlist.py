from pydantic import BaseModel, HttpUrl, Field
from typing import List


class Videos(BaseModel):
    id: str
    title: str
    duration: int
    url: HttpUrl
    thumbnail: str | None = None


class Playlist(BaseModel):
    title: str
    count_videos: int
    thumbnail: str | None
    videos: List[Videos] = Field(ge=0, le=50)


class PlaylistCreate(BaseModel):
    url: HttpUrl
