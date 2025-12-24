from yt_dlp import YoutubeDL
from app.core.progress import progress_store


def make_progress_hook(job_id: str):
    def hook(d):
        if d["status"] == "downloading":
            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes") or d.get("total_bytes_estimate")

            if total:
                percent = int(downloaded / total * 50)
                progress_store[job_id] = {"stage": "downloading", "percent": percent}

        elif d["status"] == "finished":
            progress_store[job_id] = {"stage": "zipping", "percent": 50}

    return hook


def download_urls(urls: list[str], output_template: str, job_id: str):
    total_videos = len(urls)
    completed_videos = 0
    known_total_bytes = 0
    downloaded_bytes_global = 0


    def make_progress_hook():
        nonlocal completed_videos

        def hook(d):
            nonlocal completed_videos

            if d["status"] == "downloading":
                nonlocal known_total_bytes, downloaded_bytes_global


                downloaded = d.get("downloaded_bytes", 0)
                total = d.get("total_bytes") or d.get("total_bytes_estimate")

                if total:
                    known_total_bytes += max(0, total - known_total_bytes)

                downloaded_bytes_global = sum(
                    progress_store.get(job_id, {}).get("bytes_downloaded", 0)
                    for _ in [0]
                ) + downloaded

                percent = int((downloaded_bytes_global / max(known_total_bytes, 1)) * 50)

                progress_store[job_id] = {
                    "stage": "downloading",
                    "current": completed_videos + 1,
                    "total": total_videos,
                    "bytes_downloaded": downloaded_bytes_global,
                    "bytes_total": known_total_bytes,
                    "percent": min(percent, 50),
                }

            elif d["status"] == "finished":
                completed_videos += 1


        return hook

    ydl_opts = {
        "outtmpl": output_template,
        "format": "bv*+ba/b",
        "merge_output_format": "mp4",
        "quiet": True,
        "progress_hooks": [make_progress_hook()],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)
