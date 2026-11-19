import os
from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from app.core.jobs import job
from app.schemas.download import SelectedVideosPayload
from app.schemas.playlist import PlaylistCreate
from app.services.job_runner import start_job
from app.utils.file_cleaner import cleanup_files

downloads_router = APIRouter(prefix="/downloads", tags=["Downloads"])

@downloads_router.post("/playlist")
def download_full_playlist(payload: PlaylistCreate):
    job_id = start_job([str(payload.url)], noplaylist=False)
    return {"job_id": job_id}


@downloads_router.post("/videos")
async def start_download(payload: SelectedVideosPayload):
    job_id = start_job([str(v.url) for v in payload.videos], noplaylist=True)
    return {"job_id": job_id}


@downloads_router.get("/download/{job_id}")
def download_zip(job_id: str, background_tasks: BackgroundTasks):
    folder = job.get_folder(job_id)

    if not folder:
        raise HTTPException(status_code=404, detail="Job não encontrado")

    is_delivered = job.get_job(job_id)
    if not is_delivered or is_delivered.get("delivered") == True:
        raise HTTPException(status_code=410, detail="Esse job já foi concluido e entregue")

    stage = job.get_progress(job_id)

    if not stage or stage.get("stage") != "done":
        raise HTTPException(status_code=409, detail="Download ainda não concluído")

    zip_path = f"{folder}.zip"
    if not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="ZIP não pronto")

    background_tasks.add_task(cleanup_files, folder, zip_path)

    job.is_done(job_id)

    return FileResponse(
        path=zip_path, media_type="application/zip", filename="videos.zip"
    )


@downloads_router.get("/progress/{job_id}")
def get_progress(job_id: str):
    return job.get_progress(job_id)
