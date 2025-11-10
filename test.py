import cv2
import numpy as np
import os
import matplotlib.pyplot as plt


def video_to_voxel(video_path, resize_dim=(128, 128), max_frames=None, grayscale=True):
    """
    Converts a video into a 3D voxel volume: (H, W, T)

    Parameters:
        video_path (str): Path to the video file.
        resize_dim (tuple): (width, height) to resize each frame to.
        max_frames (int): Max number of frames to process (None = all frames).
        grayscale (bool): Convert frames to grayscale.

    Returns:
        volume (np.ndarray): 3D numpy array of shape (H, W, T)
    """

    cap = cv2.VideoCapture(video_path)
    frames = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret or (max_frames is not None and frame_count >= max_frames):
            break

        if grayscale:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # (optional)

        frame = cv2.resize(frame, resize_dim)
        frames.append(frame)
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows() # Added to close any OpenCV windows

    if len(frames) == 0:
        print(f"Warning: No frames read from video {video_path}. Returning None.")
        return None

    # Stack frames. For grayscale, shape is (H, W, T). For color, it would be (H, W, C, T)
    volume = np.stack(frames, axis=-1)
    return volume

# Define the directory where the videos are located
video_directory = "/home/harshit/Xtreme_GS/data/composer_" # Replace with your directory

# List of camera names/prefixes
camera_names = ["cam01", "cam02", "cam03", "cam04", "cam05", "cam06", "cam07", "cam08"] # Add more camera names as needed

# Dictionary to store the voxel volumes for each camera
voxel_volumes = {}

# Process each video
for cam_name in camera_names:
    video_path = os.path.join(video_directory, f"{cam_name}.MP4") # Assuming .MP4 extension
    if os.path.exists(video_path):
        print(f"Processing video: {video_path}")
        try:
            # Adjust resize_dim and max_frames as needed for your videos
            volume = video_to_voxel(video_path, resize_dim=(404, 720), max_frames=600)
            if volume is not None:
                voxel_volumes[cam_name] = volume
                print(f"Voxel volume shape for {cam_name}: {volume.shape}")
            else:
                print(f"Could not generate voxel volume for {cam_name}")
        except Exception as e:
            print(f"An error occurred while processing {video_path}: {e}")
    else:
        print(f"Video not found: {video_path}")

# Now WE can access the voxel volumes for each camera using the voxel_volumes dictionary
# For example:
# cam01_volume = voxel_volumes.get("cam01")
# cam02_volume = voxel_volumes.get("cam02")
# ...
