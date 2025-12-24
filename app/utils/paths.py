import os
import uuid

DOWNLOAD_ROOT = "downloads"


def create_playlist_dir() -> str:
    folder = f"playlist_{uuid.uuid4().hex}"
    path = os.path.join(DOWNLOAD_ROOT, folder)
    os.makedirs(path, exist_ok=True)
    return path
