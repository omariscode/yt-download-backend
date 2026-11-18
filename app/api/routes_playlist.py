from fastapi import APIRouter, HTTPException
from app.schemas.playlist import Playlist, Videos, PlaylistCreate
from app.services import analyze_playlist

playlist_router = APIRouter(prefix="/playlists", tags=["Playlists"])


@playlist_router.post("/", response_model=Playlist)
def analyze_playlist_route(payload: PlaylistCreate):
    """
    Rota para analisar uma playlist do YouTube e retornar os detalhes.
    """
    try:
        data = analyze_playlist(payload.url)

        videos = [
            Videos(
                id=video["id"],
                title=video["title"],
                duration=video["duration"] or 0,
                url=video["url"],
                thumbnail=video["thumbnail"],
            )
            for video in data.get("videos", [])
        ]

        return Playlist(
            title=data.get("title") or "",
            count_videos=len(videos),
            videos=videos,
            thumbnail=data.get("thumbnail"),
        )

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Erro ao analisar playlist: {str(e)}"
        )
