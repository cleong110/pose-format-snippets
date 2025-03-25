from typing import List
from pose_format_snippets.utils.pose_files import load_pose_data, add_z_offsets_to_pose

import plotly.graph_objects as go


# def plot_xyz(positions):
#     # Unzip the list of positions into X, Y, Z components
#     X, Y, Z = zip(*positions)

#     # Create a 3D scatter plot
#     fig = go.Figure(data=[go.Scatter3d(x=X, y=Y, z=Z, mode="markers", marker=dict(size=5, color="blue"))])

#     # Update layout
#     fig.update_layout(scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"), title="3D XYZ Plot")

#     # Show the plot
#     fig.show()


def plot_xyz(positions_list, labels_list, components_list: List):
    # Create an empty figure
    fig = go.Figure()

    # Iterate through each list of positions and add a trace
    for i, positions in enumerate(positions_list):
        # Unzip the list of positions into X, Y, Z components
        X, Y, Z = zip(*positions)

        # Add a scatter trace for each list of positions with a different color
        component_name = labels_list[i][0]
        if component_name in components_list:
            trace_color_index = components_list.index(component_name)
            trace_color = dict(
                size=5,
                color=f"rgb({(trace_color_index*50)%255}, {(trace_color_index*100)%255}, {(trace_color_index*150)%255})",
            )  # Different color for each list
        else:

            trace_color = dict(
                size=5, color=f"rgb({(i*50)%255}, {(i*100)%255}, {(i*150)%255})"
            )  # Different color for each list
        fig.add_trace(
            go.Scatter3d(
                x=X,
                y=Y,
                z=Z,
                mode="markers",
                marker=trace_color,
                name=f"{labels_list[i]}",  # Label each trace
            )
        )

    # Update layout
    fig.update_layout(scene=dict(xaxis_title="X", yaxis_title="Y", zaxis_title="Z"), title="Pose with XYZ")

    # Show the plot
    fig.show()


if __name__ == "__main__":
    pose = load_pose_data(r"test_poses\poses_with_refine_face_landmarks\WIN_20240904_12_20_56_Pro-SAD.pose")

    # pose = add_z_offsets_to_pose(pose)
    pose = pose.normalize()
    pose = pose.get_components(["LEFT_HAND_LANDMARKS", "RIGHT_HAND_LANDMARKS"])

    xyz_positions = []
    xyz_labels = []
    components = []

    # build index to label mapping
    index_to_label_mapping = {}
    for c in pose.header.components:
        components.append(c.name)
        for p in c.points:
            index = pose.header.get_point_index(c.name, p)
            index_to_label_mapping[index] = (c.name, p)

    for i, keypoint_trajectory in enumerate(pose.body.points_perspective().squeeze()):
        print(keypoint_trajectory.shape)

        xyz_positions.append(keypoint_trajectory)
        label = index_to_label_mapping[i]
        xyz_labels.append(label)
    #     for person in frame:
    #         print(person.shape)  # (586, 3)
    #         keypoint_0 = person[0]
    #         print(keypoint_0)
    #         xyz_positions.append(keypoint_0)
    components = list(set(components))
    plot_xyz(xyz_positions, xyz_labels, components_list=components)
