import os
from dotenv import load_dotenv

load_dotenv()

DOWNLOAD_ROOT = os.getenv("DOWNLOAD_ROOT", "/tmp/downloads")
JOB_TTL_SECONDS = int(os.getenv("JOB_TTL_SECONDS", "3600"))
CORS_ALLOWED_ORIGINS = [
    origem.strip()
    for origem in os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    if origem.strip()
]
