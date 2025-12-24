import shutil
import os


def cleanup_files(folder: str, zip_path: str = None):
    if os.path.exists(folder):
        shutil.rmtree(folder)

    if zip_path and os.path.exists(zip_path):
        os.remove(zip_path)
