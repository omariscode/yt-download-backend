from yt_dlp import YoutubeDL

def analyze_playlist(url: str) -> dict:
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        "title": info.get("title"),
        "video_count": len(info.get("entries", [])),
        "videos": [
            {
                "id": v.get("id"),
                "title": v.get("title"),
                "url": v.get("url"),
                "duration": v.get("duration"),
                "thumbnail": v.get("thumbnail")
            }
            for v in info.get("entries", [])
        ]
    }
