from pathlib import Path
from typing import List, Optional

import gdown


def download_poses(gdrive_ids: List[str], download_folder: Path):
    """Download multiple files from Google Drive given their file IDs."""
    download_folder.mkdir(parents=True, exist_ok=True)

    for file_id in gdrive_ids:
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, str(download_folder / f"{file_id}.zip"), quiet=False)


def download_default_poses(folder_id: Optional[str] = None, out_folder: Optional[Path] = None):
    """Download all files from the default Google Drive folder."""
    if folder_id is None:
        folder_id = (
            r"16GERa5DND7a6_3mf2ARdSfzTCBeVlbsS"  # ASL Citizen words signed by Colin Leong, with refine_landmarks
        )
    folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
    gdown.download_folder(folder_url, output=out_folder, quiet=False)
