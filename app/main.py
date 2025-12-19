from fastapi import FastAPI
from app.api.v1.routes_playlist import router as playlist_router
from app.api.v1.routes_tasks import router as task_router

app = FastAPI(title="YT Playlist Downloader")

app.include_router(playlist_router, prefix="/api/v1")
app.include_router(task_router, prefix="/api/v1")
