from yt_dlp import YoutubeDL

def download_urls(
    urls: list[str],
    output_template: str,
    progress_hook=None
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
    }

    if progress_hook:
        ydl_opts["progress_hooks"] = [progress_hook]

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)
