from typing import Any
from urllib.parse import urljoin

from yt_dlp import YoutubeDL

YOUTUBE_BASE = "https://www.youtube.com/"
THUMBNAIL_BASE = "https://i.ytimg.com/"


def _absoluta(raw: object, base: str) -> str | None:
    if not isinstance(raw, str) or not raw:
        return None

    if raw.startswith("//"):
        return f"https:{raw}"

    return urljoin(base, raw)


def analyze_playlist(url: str) -> dict[str, Any]:
    """
    Analisa o link da playlist e retorna os vídeos com thumbnails
    """
    ydl_opts: Any = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    entries = info.get("entries") or []
    playlist_thumbnail = _absoluta(info.get("thumbnail"), THUMBNAIL_BASE)

    videos: list[dict[str, Any]] = []
    for entry in entries:
        video_id = entry.get("id")
        if not video_id:
            continue

        video_url = _absoluta(entry.get("url"), YOUTUBE_BASE)
        if not video_url:
            video_url = f"{YOUTUBE_BASE}watch?v={video_id}"

        thumb = _absoluta(entry.get("thumbnail"), THUMBNAIL_BASE)
        if not thumb:
            thumb = f"{THUMBNAIL_BASE}vi/{video_id}/hqdefault.jpg"

        videos.append(
            {
                "id": str(video_id),
                "title": entry.get("title") or "",
                "url": video_url,
                "duration": entry.get("duration") or 0,
                "thumbnail": thumb,
            }
        )

    return {
        "id": info.get("id"),
        "title": info.get("title") or "",
        "thumbnail": playlist_thumbnail,
        "video_count": len(videos),
        "videos": videos,
    }
