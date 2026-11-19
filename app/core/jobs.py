from pydantic import BaseModel, Field
from typing import Literal
import threading
import time
import uuid
from app.core.config import JOB_TTL_SECONDS

class ProgressState(BaseModel):
    stage: Literal["starting", "downloading", "zipping", "done", "error"] = "starting"
    percent: int = Field(default=0, ge=0, le=100)
    current: int = 0
    total: int = 0
    bytes_downloaded: int = 0
    total_bytes: int = 0
    error: str | None = None
    revision: int = 0

class JobStore:
    def __init__(self):
        self._lock = threading.RLock()
        self._jobs: dict[str, dict] = {}

    def create(self, folder: str) -> str:
        job_id = uuid.uuid4().hex

        with self._lock:
            self._jobs[job_id] = {
                "folder": folder,
                "state": ProgressState(),
                "created_at": time.monotonic(),
                "delivered": False,
            }
        return job_id

    def update(self, job_id: str, **changes) -> None:
        with self._lock:
            state = self._jobs[job_id]["state"]
            updated = state.model_copy(update={**changes, "revision": state.revision + 1})
            self._jobs[job_id]["state"] = updated

    def get_job(self, job_id: str):
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                return None
            return job.copy()

    def get_progress(self, job_id: str) -> dict | None:
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                return None
            return job["state"].model_dump()

    def get_folder(self, job_id) -> str | None:
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                return None
            return job["folder"]

    def is_done(self, job_id: str) -> dict | None:
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                return None
            job["delivered"] = True
            return job["state"].model_dump()

    def failed(self, job_id: str, msg: str) -> None:
        with self._lock:
            if job_id not in self._jobs:
                return
            self.update(job_id, stage="error", percent=0, error=msg)


job = JobStore()
