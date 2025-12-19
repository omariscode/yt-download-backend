from fastapi import APIRouter, HTTPException
from app.schemas.playlist import Playlist, Videos
from app.services import analyze_playlist

playlist_router = APIRouter(prefix="/playlists", tags=["Playlists"])

@playlist_router.post("/", response_model=Playlist)
def analyze_playlist_route(url: str):
    try:
        data = analyze_playlist(url)

        videos = [
            Videos(
                id=video["id"],
                title=video["title"],
                duration=video["duration"] or 0,
            )
            for video in data.get("videos", [])
        ]

        return Playlist(
            title=data.get("title"),
            count_videos=len(videos),
            videos=videos,
            thumbnail=data.get("thumbnail")

        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao analisar playlist: {str(e)}"
        )
