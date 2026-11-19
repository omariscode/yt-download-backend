import logging
import threading
from app.core.jobs import job
from app.services.playlist_download import download_urls
from app.utils.paths import create_playlist_dir
from app.utils.zip import zip_folder_with_progress

logger = logging.getLogger(__name__)


def start_job(urls: list[str], *, noplaylist: bool) -> str:
    """Inicia um job para fazer o download de cada vídeo associado as urls.
        Params:
            urls -> Lista de urls de uma playlist
            noplaylist -> Boolean para saber se é um vídeo individual ou playlist
    """
    folder = create_playlist_dir()
    job_id = job.create(folder)

    def run() -> None:
        try:
            download_urls(
                urls=urls,
                output_template=f"{folder}/%(title)s.%(ext)s",
                job_id=job_id,
                noplaylist=noplaylist,
            )
            zip_folder_with_progress(folder, job_id)
        except Exception:
            logger.exception(f"Falha no job {job_id}")
            job.failed(job_id, "Falha no download")
        finally:
            state = job.get_progress(job_id)
            if state is not None and state["stage"] not in {"done", "error"}:
                job.failed(job_id, "Job encerrado sem estado final")

    threading.Thread(target=run, daemon=True).start()
    return job_id
