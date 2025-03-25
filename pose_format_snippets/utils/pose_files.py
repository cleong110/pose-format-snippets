from itertools import chain
from pathlib import Path
from typing import Iterator, Union

import numpy.ma as ma

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


def add_z_offsets_to_pose(pose: Pose, speed: float = 1.0) -> Pose:

    offset = speed / pose.body.fps
    # Assuming pose.data is a numpy masked array
    pose_data = pose.body.data  # Shape: (frames, persons, keypoints, xyz)

    # Create an offset array that only modifies the Z-dimension (index 2)
    offsets = ma.arange(pose_data.shape[0]).reshape(-1, 1, 1, 1) * offset

    # Apply the offsets only to the Z-axis (index 2), preserving masks
    pose_data[:, :, :, 2] += offsets[:, :, :, 0]

    pose.body.data = pose_data
    return pose
