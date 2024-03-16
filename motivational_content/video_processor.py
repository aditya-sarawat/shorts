# motivational_content/video_processor.py
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio
import requests
from moviepy.editor import VideoFileClip, AudioFileClip
from motivational_content.helper import generate_unique_filename
from moviepy.video.fx.all import mirror_x

BASE_PATH = "./motivational_content/__temp__/"
TEMP_VIDEO_PATH = "./motivational_content/__temp__/temp_video.mp4"


def download_video(video_url):
    try:
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        block_size = 2048
        with open(TEMP_VIDEO_PATH, "wb") as video_file:
            for data in response.iter_content(block_size):
                video_file.write(data)
        return True
    except requests.exceptions.RequestException as e:
        return False


def trim_and_rename_video(video_path, target_duration):
    temp_path = BASE_PATH + "trimmer.mp4"
    video_clip = VideoFileClip(video_path)
    trimmed_clip = video_clip.subclip(0, target_duration)
    trimmed_clip.write_videofile(
        temp_path, codec="libx264", audio_codec="aac", verbose=False, logger=None
    )
    video_clip.close()
    trimmed_clip.close()
    os.rename(temp_path, video_path)


def check_and_process_video_for_quote(video_path, quote):
    try:
        video_duration = VideoFileClip(video_path).duration
        quote_length = len(quote.split())
        required_duration = max((quote_length * 0.8) + 4, 15)
        if video_duration < required_duration:
            pass
        else:
            trim_and_rename_video(video_path, target_duration=required_duration)
        return video_duration, required_duration
    except Exception as e:
        pass


def crop_and_resize_video(video_path, output_path, target_width, target_height):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = imageio.get_writer(output_path, fps=fps, macro_block_size=None)

    target_aspect_ratio = target_width / target_height
    crop_width = min(original_width, int(original_height * target_aspect_ratio))
    crop_start = (original_width - crop_width) // 2
    crop_end = crop_start + crop_width

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

    out.close()
    cap.release()


def apply_blur(frame, blur_strength=2.0):
    return cv2.GaussianBlur(frame, (0, 0), blur_strength)


def apply_blur_to_video(video_path, output_path, blur_strength):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    out = imageio.get_writer(output_path, fps=fps, macro_block_size=None)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_with_blur = apply_blur(frame_rgb, blur_strength)

        out.append_data(frame_with_blur)

    out.close()
    cap.release()


def add_overlay(frame_pil):
    overlay = Image.new("RGBA", frame_pil.size, (0, 0, 0, int(255 * 0.4)))
    frame_pil = Image.alpha_composite(frame_pil.convert("RGBA"), overlay)
    return frame_pil.convert("RGB")


def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height


def add_text_to_frame(frame, text, font, video_dimensions, duration, video_length):
    draw = ImageDraw.Draw(frame)
    max_width = video_dimensions[0] * 0.8

    lines = []
    current_line = ""
    for word in text.split():
        test_line = current_line + word + " "
        test_width, _ = textsize(test_line, font)

        if test_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    total_text_height = sum([textsize(line, font)[1] for line in lines])
    y_position = (video_dimensions[1] - total_text_height) // 2

    total_duration = 0.0
    for line in lines:
        words_in_line = len(line.split())
        line_duration = (video_length - duration) / len(lines)
        text_width, text_height = textsize(line, font)

        if text_width > video_dimensions[0]:
            scale_factor = video_dimensions[0] / text_width
            new_font_size = int(font.size * scale_factor)
            font_resized = ImageFont.truetype(font.path, new_font_size)
        else:
            font_resized = font

        text_width_resized, text_height_resized = textsize(line, font_resized)
        x_position = (video_dimensions[0] - text_width_resized) // 2
        draw.text(
            (x_position, y_position), line, font=font_resized, fill=(255, 255, 255, 255)
        )
        y_position += text_height_resized
        total_duration += line_duration

        if total_duration >= (video_length - duration):
            break

    return np.array(frame)


def process_cropped_video(video_path, quote, selected_font, video_length):
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        output_path = os.path.join(BASE_PATH, "quote_video.mp4")
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
            frame_pil = add_overlay(frame_pil)
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
    except Exception as e:
        pass


def combine_audio_video(audio_path, video_path):
    try:
        audio = AudioFileClip(audio_path)
        video = VideoFileClip(video_path)
        audio = audio.set_duration(video.duration)
        video_with_audio = video.set_audio(audio)
        output_path = os.path.join("./reels", generate_unique_filename("mp4"))
        video_with_audio.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            fps=video.fps,
            verbose=False,
            logger=None,
        )
        return output_path
    except Exception as e:
        pass
