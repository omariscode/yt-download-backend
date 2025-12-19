from celery import Celery
from app.core.config import REDIS_URL

celery_app = Celery(
    "yt_downloader",
    broker=REDIS_URL,
    backend=REDIS_URL
)
