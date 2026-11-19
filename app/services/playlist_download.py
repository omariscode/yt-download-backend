from typing import Any

from yt_dlp import YoutubeDL
from app.core.jobs import job

def make_progress_hook(job_id: str):
    def hook(d: dict):
        if d["status"] == "downloading":
            downloaded = d.get("bytes_downloaded", 0)
            total = d.get("total_bytes")

            if total:
                percent = int(downloaded / total * 50)
                job.update(job_id, stage="downloading", percent=percent)

        elif d["status"] == "finished":
            job.update(job_id, stage="zipping", percent=50)

    return hook


def download_urls(
    urls: list[str], output_template: str, job_id: str, noplaylist: bool = False
):
    total_videos = len(urls)
    completed_videos = 0
    known_total_bytes = 0
    downloaded_bytes_global = 0


    def make_progress_hook():
        nonlocal completed_videos

        def hook(d:dict):
            nonlocal completed_videos

            if d["status"] == "downloading":
                nonlocal known_total_bytes, downloaded_bytes_global


                downloaded = d.get("bytes_downloaded", 0)
                total = d.get("total_bytes")

                if total:
                    known_total_bytes += max(0, total - known_total_bytes)

                downloaded_bytes_global = sum(
                    (job.get_progress(job_id) or {}).get("bytes_downloaded", 0)
                    for _ in [0]
                ) + downloaded

                percent = int((downloaded_bytes_global / max(known_total_bytes, 1)) * 50)

                job.update(job_id, stage="downloading",
                           current=completed_videos + 1,
                           total = total_videos,
                           bytes_downloaded = downloaded_bytes_global,
                           total_bytes = known_total_bytes,
                           percent = min(percent, 50)
                        )

            elif d["status"] == "finished":
                completed_videos += 1


        return hook

    ydl_opts: Any = {
        "outtmpl": output_template,
        "format": "bv*+ba/b",
        "merge_output_format": "mp4",
        "quiet": True,
        "noplaylist": noplaylist,
        "progress_hooks": [make_progress_hook()],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)
