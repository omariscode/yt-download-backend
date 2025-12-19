from fastapi import APIRouter, HTTPException
from app.workers.downloader import download_full_playlist_task, download_selected_videos_task

downloads_router = APIRouter(prefix="/downloads", tags=["Downloads"])

@downloads_router.post("/playlist")
def download_full_playlist(playlist_url: str):
    try:
        task = download_full_playlist_task.delay(playlist_url)

        return {
            "message": "Download da playlist iniciado",
            "task_id": task.id
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao iniciar download da playlist: {str(e)}"
        )

@downloads_router.post("/videos")
def download_selected_videos(video_urls: list[str]):
    try:
        task = download_selected_videos_task.delay(video_urls)

        return {
            "message": "Download dos vídeos iniciado",
            "task_id": task.id,
            "total_videos": len(video_urls)
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao iniciar download dos vídeos: {str(e)}"
        )
