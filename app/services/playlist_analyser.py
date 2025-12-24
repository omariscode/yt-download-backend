from yt_dlp import YoutubeDL


def analyze_playlist(url: str) -> dict:
    """
    Analisa o link da playlist e retorna os vídeos com thumbnails
    """
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    entries = info.get("entries", [])

    playlist_thumbnail = info.get("thumbnail")

    videos = []
    for v in entries:
        video_id = v.get("id")
        thumb = v.get("thumbnail") or f"i.ytimg.com{video_id}/hqdefault.jpg"

        videos.append(
            {
                "id": video_id,
                "title": v.get("title"),
                "url": v.get("url") or f"www.youtube.com{video_id}",
                "duration": v.get("duration"),
                "thumbnail": thumb,
            }
        )

    return {
        "id": info.get("id"),
        "title": info.get("title"),
        "thumbnail": playlist_thumbnail,
        "video_count": len(videos),
        "videos": videos,
    }
