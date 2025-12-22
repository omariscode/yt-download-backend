from app.services.playlist_download import download_urls
from app.utils.paths import create_playlist_dir
from app.utils.zip import zip_folder_stream

def download_full_playlist_task(playlist_url: str):
    """
    Baixa playlist inteira e compacta em ZIP
    """
    playlist_dir = create_playlist_dir()

    download_urls(
        urls=[playlist_url],
        output_template=f"{playlist_dir}/%(title)s.%(ext)s",
    )

    zip_path = zip_folder_stream(playlist_dir)

    return {
        "status": "done",
        "zip_path": zip_path
    }

def download_selected_videos_task(
    video_urls: list[str]
):
    """
    Baixa apenas vídeos selecionados
    """
    playlist_dir = create_playlist_dir()

    download_urls(
        urls=video_urls,
        output_template=f"{playlist_dir}/%(title)s.%(ext)s",
    )

    return playlist_dir
