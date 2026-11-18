import os
import uuid
from app.core.config import DOWNLOAD_ROOT


def create_playlist_dir() -> str:
    folder = f"playlist_{uuid.uuid4().hex}"
    path = os.path.join(DOWNLOAD_ROOT, folder)
    os.makedirs(path, exist_ok=True)
    return path
