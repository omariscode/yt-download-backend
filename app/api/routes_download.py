import asyncio
import uuid
import os
from app.utils.zip import zip_folder_stream
from fastapi import APIRouter, HTTPException
from fastapi import BackgroundTasks
from fastapi.responses import FileResponse
from fastapi import BackgroundTasks
from app.utils.paths import create_playlist_dir
from app.services.playlist_download import download_urls
from fastapi.responses import StreamingResponse
from app.utils.file_cleaner import cleanup_files
from app.utils.zip import zip_folder_with_progress
from app.schemas.download import SelectedVideosPayload
from app.workers.downloader import download_full_playlist_task
from app.core.progress import progress_store, job_to_folder

downloads_router = APIRouter(prefix="/downloads", tags=["Downloads"])

@downloads_router.post("/playlist")
def download_full_playlist(playlist_url: str):
    try:
        zip_path = download_full_playlist_task(playlist_url)

        return FileResponse(
            path=zip_path,
            media_type="application/zip",
            filename="playlist.zip"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao iniciar download da playlist: {str(e)}"
        )


@downloads_router.post("/videos")
async def start_download(payload: SelectedVideosPayload):
    job_id = uuid.uuid4().hex
    folder = create_playlist_dir()

    job_to_folder[job_id] = folder
    progress_store[job_id] = {"stage": "starting", "percent": 0}

    video_urls = [v.url for v in payload.videos]

    async def run():
        download_urls(
            urls=video_urls,
            output_template=f"{folder}/%(title)s.%(ext)s",
            job_id=job_id
        )
        zip_folder_with_progress(folder, job_id)

    asyncio.create_task(run())

    return {"job_id": job_id}

@downloads_router.get("/download/{job_id}")
def download_zip(job_id: str, background_tasks: BackgroundTasks):
    folder = job_to_folder.get(job_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Job não encontrado")

    zip_path = f"{folder}.zip"
    if not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="ZIP não pronto")

    background_tasks.add_task(cleanup_files, folder, zip_path)

    return FileResponse(
        path=zip_path,
        media_type="application/zip",
        filename="videos.zip"
    )

@downloads_router.get("/progress/{job_id}")
def get_progress(job_id: str):
    return progress_store.get(job_id, {"status": "unknown"})
