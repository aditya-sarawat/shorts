import os
import cv2
import imageio
from util.logger import get_logger

logger = get_logger()


def apply_blur(frame, blur_strength=2.0):
    try:
        # Apply Gaussian blur effect to the frame
        return cv2.GaussianBlur(frame, (0, 0), blur_strength)
    except Exception as e:
        logger.error(f"Error applying blur effect: {e}")
        return frame


def apply_blur_to_video(video_path, output_path, blur_strength):
    try:
        # Open the video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise IOError(f"Failed to open video file: {video_path}")

        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Initialize output video writer
        out = imageio.get_writer(output_path, fps=fps, macro_block_size=None)

        # Read frames, apply blur, and write to output video
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Apply blur effect to the frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_with_blur = apply_blur(frame_rgb, blur_strength)

            # Append to output video
            out.append_data(frame_with_blur)

        # Release resources
        out.close()
        cap.release()

        logger.info(f"Blur effect applied successfully. Output saved to: {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error applying blur to video: {e}")
        return False
