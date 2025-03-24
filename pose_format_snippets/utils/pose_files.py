from itertools import chain
from pathlib import Path
from typing import Iterator, Union

from pose_format import Pose
from pose_format.pose_header import PoseHeaderCache
from pyzstd import decompress


def get_pose_file_paths(directory: Path | str) -> Iterator[Path]:
    """
    Lazily finds all '.pose' files in the given directory.
    """
    directory = Path(directory)
    return chain(directory.rglob("*.pose"), directory.rglob("*.pose.zst"))


def get_actual_pose_stem(filename: Path | str) -> str:
    """Extracts the actual stem, ensuring .pose or .pose.zst is properly handled."""
    stem = Path(filename).stem  # Get the initial stem
    return Path(stem).stem if stem.endswith(".pose") else stem  # Strip another layer if needed


def load_pose_data(file_path: Union[Path, str]) -> Pose:
    """Loads a .pose or .pose.zst, returns a Pose object"""
    file_path = Path(file_path)
    if file_path.name.endswith(".pose.zst"):
        print(f"ZST: {file_path}")
        try:
            return Pose.read(decompress(file_path.read_bytes()))
        except RuntimeError as e:
            if "PoseHeaderCache hash does not match buffer hash" in str(e):
                PoseHeaderCache.start_offset = None
                PoseHeaderCache.end_offset = None
                PoseHeaderCache.hash = None
                PoseHeaderCache.header = None
                return Pose.read(decompress(file_path.read_bytes()))
    return Pose.read(file_path.read_bytes())
