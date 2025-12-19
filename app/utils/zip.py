import os
import zipfile

def zip_folder(folder_path: str) -> str:
    zip_path = f"{folder_path}.zip"

    with zipfile.ZipFile(zip_path, "w") as zf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full = os.path.join(root, file)
                zf.write(full, arcname=file)

    return zip_path
