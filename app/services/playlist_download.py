from yt_dlp import YoutubeDL
from app.core.progress import progress_store

def make_progress_hook(job_id: str):
    def hook(d):
        if d["status"] == "downloading":
            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes") or d.get("total_bytes_estimate")

            if total:
                percent = int(downloaded / total * 50)
                progress_store[job_id] = {
                    "stage": "downloading",
                    "percent": percent
                }

        elif d["status"] == "finished":
            progress_store[job_id] = {
                "stage": "zipping",
                "percent": 50
            }

    return hook


def download_urls(
    urls: list[str],
    output_template: str,
    job_id: str
):
    """
    Faz download de uma lista de URLs
    """
    ydl_opts = {
        "quiet": True,
        "ignoreerrors": True,
        "restrictfilenames": True,
        "outtmpl": output_template,
        "format": "bv*+ba/b",
        "merge_output_format": "mp4",
        "progress_hooks": [make_progress_hook(job_id)],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)
