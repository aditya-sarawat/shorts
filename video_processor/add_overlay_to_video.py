import os
import cv2
import numpy as np
from PIL import Image, ImageFont
import imageio
from util.logger import get_logger

logger = get_logger()
BASE_PATH = "./__temp__/"


def add_overlay(frame_pil):
    try:
        overlay = Image.new("RGBA", frame_pil.size, (0, 0, 0, int(255 * 0.4)))
        frame_pil = Image.alpha_composite(frame_pil.convert("RGBA"), overlay)
        return frame_pil.convert("RGB")
    except Exception as e:
        logger.error(f"Error adding overlay to frame: {e}")
        return frame_pil


def add_overlay_to_video(video_path, output_path):
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        out = imageio.get_writer(output_path, fps=fps, macro_block_size=None)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb)
            frame_with_overlay = add_overlay(frame_pil)

            out.append_data(np.array(frame_with_overlay))

        out.close()
        cap.release()
        logger.info(f"Overlay added successfully. Output saved to: {output_path}")
    except Exception as e:
        logger.error(f"Error adding overlay to video: {e}")
