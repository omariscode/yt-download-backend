import os
import zipfile
from app.core.jobs import job


def zip_folder_with_progress(folder_path: str, job_id: str) -> str:
    """
    Cria um arquivo ZIP da pasta especificada, atualizando o progresso do job
    """
    zip_path = f"{folder_path}.zip"
    files = []

    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    total_files = len(files)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for i, file_path in enumerate(files):
            zipf.write(file_path, arcname=os.path.basename(file_path))

            job.update(job_id,
                       stage="zipping",current=i+1,
                       total=total_files,
                       bytes_downloaded=i+1,
                       total_bytes=total_files,
                       percent=50 + int((i + 1) / total_files * 50)
                    )


    job.update(job_id, stage="done",
               current=total_files,
               bytes_downloaded=total_files,
               total_bytes=total_files,
               percent=100
            )

    return zip_path
