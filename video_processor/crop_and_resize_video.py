import os
import cv2
import imageio
from util.logger import get_logger

logger = get_logger()


def crop_and_resize_video(video_path, output_path, target_width, target_height):
    try:
        # Open the video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise IOError(f"Failed to open video file: {video_path}")

        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Calculate cropping parameters
        target_aspect_ratio = target_width / target_height
        crop_width = min(original_width, int(original_height * target_aspect_ratio))
        crop_start = (original_width - crop_width) // 2
        crop_end = crop_start + crop_width

        # Initialize output video writer
        out = imageio.get_writer(output_path, fps=fps, macro_block_size=None)

        # Read, crop, and resize frames
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_cropped = cv2.resize(
                frame_rgb[:, crop_start:crop_end], (target_width, target_height)
            )
            frame_resized = cv2.cvtColor(frame_cropped, cv2.COLOR_BGR2BGRA)

            out.append_data(frame_resized)

        # Release resources
        out.close()
        cap.release()

        logger.info(
            f"Video cropped and resized successfully. Output saved to: {output_path}"
        )
        return True
    except Exception as e:
        logger.error(f"Error cropping and resizing video: {e}")
        return False
