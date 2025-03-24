from pathlib import Path
import random
from pose_format_snippets.gdrive.gdrive_utils import download_default_poses
from pose_format_snippets.utils.pose_files import get_pose_file_paths, load_pose_data, get_actual_pose_stem

if __name__ == "__main__":
    # download_default_poses()

    # ASL Citizen "SAIL" as .pose.zst files
    # download_default_poses("1xrRNY90nnfNRtFkr3KQIOKveLNxKQxaK")

    dir_to_search = r"ASL_CITIZEN_SAIL_poses"
    dir_to_search = r"poses_with_refine_face_landmarks"
    dir_to_search = r"test_poses"
    # dir_to_search = Path.cwd()

    pose_paths = list(get_pose_file_paths(dir_to_search))
    # random.shuffle(pose_paths)

    for pose_path in pose_paths:
        print(pose_path)
        print(get_actual_pose_stem(pose_path))
        pose = load_pose_data(pose_path)
        print(pose.body.data.shape)
