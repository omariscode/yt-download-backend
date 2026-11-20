from typing import Any

from yt_dlp import YoutubeDL

from app.core.jobs import job


def download_urls(
    urls: list[str], output_template: str, job_id: str, noplaylist: bool = False
):
    total_videos = len(urls)

    arquivos: dict[str, dict[str, int]] = {}
    vistos: set[str] = set()
    ultimo_percent = 0

    def hook(d: dict) -> None:
        nonlocal ultimo_percent

        if d["status"] not in {"downloading", "finished"}:
            return

        info = d.get("info_dict") or {}
        chave = d.get("filepath") or d.get("filename") or info.get("id") or "arquivo"
        vistos.add(str(info.get("id") or chave))

        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0

            baixado = d.get("downloaded_bytes", 0)
            arquivos[chave] = {
                "downloaded": min(baixado, total) if total else baixado,
                "total": total,
            }
        else:

            atual = arquivos.get(chave, {"downloaded": 0, "total": 0})
            arquivos[chave] = {"downloaded": atual["total"], "total": atual["total"]}

        baixado_total = sum(f["downloaded"] for f in arquivos.values())
        total_global = sum(f["total"] for f in arquivos.values())

        if total_global:

            estimativa = total_global * total_videos / max(len(vistos), 1)
            calculado = int(baixado_total / estimativa * 50)

            ultimo_percent = max(ultimo_percent, min(calculado, 49))

        job.update(
            job_id,
            stage="downloading",
            current=min(len(arquivos), total_videos),
            total=total_videos,
            downloaded_bytes=baixado_total,
            total_bytes=total_global,
            percent=ultimo_percent,
        )

    ydl_opts: Any = {
        "outtmpl": output_template,
        "format": "bv*+ba/b",
        "merge_output_format": "mp4",
        "quiet": True,
        "noplaylist": noplaylist,
        "progress_hooks": [hook],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)
