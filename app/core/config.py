import os
from dotenv import load_dotenv

load_dotenv()

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")
REDIS_URL = os.getenv("REDIS_URL")
MAX_PLAYLIST_VIDEOS = int(os.getenv("MAX_PLAYLIST_VIDEOS", 50))
