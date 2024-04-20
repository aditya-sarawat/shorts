import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio
from util.logger import get_logger

logger = get_logger()


def calculate_text_size(text, font):
    try:
        im = Image.new(mode="RGB", size=(0, 0))
        draw = ImageDraw.Draw(im)
        _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
        return width, height
    except Exception as e:
        logger.error(f"Error calculating text size: {e}")
        return 0, 0


def add_text_to_frame(frame, text, font, video_dimensions, duration, video_length):
    try:
        draw = ImageDraw.Draw(frame)
        max_width = video_dimensions[0] * 0.8

        lines = []
        current_line = ""
        for word in text.split():
            test_line = current_line + word + " "
            test_width, _ = calculate_text_size(test_line, font)

            if test_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        total_text_height = sum([calculate_text_size(line, font)[1] for line in lines])
        y_position = (video_dimensions[1] - total_text_height) // 2

        total_duration = 0.0
        for line in lines:
            words_in_line = len(line.split())
            line_duration = (video_length - duration) / len(lines)
            text_width, text_height = calculate_text_size(line, font)

            if text_width > video_dimensions[0]:
                scale_factor = video_dimensions[0] / text_width
                new_font_size = int(font.size * scale_factor)
                font_resized = ImageFont.truetype(font.path, new_font_size)
            else:
                font_resized = font

            text_width_resized, text_height_resized = calculate_text_size(
                line, font_resized
            )
            x_position = (video_dimensions[0] - text_width_resized) // 2
            draw.text(
                (x_position, y_position),
                line,
                font=font_resized,
                fill=(255, 255, 255, 255),
            )
            y_position += text_height_resized
            total_duration += line_duration

            if total_duration >= (video_length - duration):
                break

        return np.array(frame)
    except Exception as e:
        logger.error(f"Error adding text to frame: {e}")
        return np.array(frame)


def add_text_to_video(video_path, output_path, quote, selected_font, video_length):
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        out = imageio.get_writer(output_path, fps=fps, macro_block_size=None)

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        font_size = min(int(original_height * 0.06), 80)
        font = ImageFont.truetype(selected_font, font_size)
        duration = 0.0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb)
            frame_with_text = add_text_to_frame(
                frame_pil,
                quote,
                font,
                (original_width, original_height),
                duration,
                video_length,
            )
            out.append_data(np.array(frame_with_text))
            duration += 1 / fps

            if duration >= video_length:
                break

        out.close()
        cap.release()
    except Exception as e:
        logger.error(f"Error adding text to video: {e}")
