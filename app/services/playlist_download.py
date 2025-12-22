from yt_dlp import YoutubeDL
from app.core.progress import progress_store

def make_progress_hook(job_id: str):
    """Progresso do download"""
    def hook(d):
        if d["status"] == "downloading":
            percent_str = d.get("_percent_str", "0%").strip("%")
            try:
                progress_store[job_id] = int(float(percent_str))
            except ValueError:
                progress_store[job_id] = 0
        elif d["status"] == "finished":
            progress_store[job_id] = 50  # Halfway, now zippingj
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
