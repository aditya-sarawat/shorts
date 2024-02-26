# motivational_content/video_processor.py
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio
import requests
from tqdm import tqdm
from moviepy.editor import VideoFileClip, concatenate_videoclips
from motivational_content.helper import generate_unique_filename

BASE_PATH = "./motivational_content/__temp__/"
TEMP_VIDEO_PATH = "./motivational_content/__temp__/temp_video.mp4"

def reverse_and_append(video_path, output_path):
    video_clip = VideoFileClip(video_path)
    reversed_clip = video_clip.fx(lambda x: x.fx(VideoFileClip.fl, 'horizontal'))
    final_clip = concatenate_videoclips([video_clip, reversed_clip])
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    video_clip.close()
    reversed_clip.close()
    final_clip.close()

def adjust_video_length(input_path, output_path, target_duration=15):
    video_clip = VideoFileClip(input_path)

    trimmed_clip = video_clip.subclip(0, target_duration)
    trimmed_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    
    video_clip.close()
    trimmed_clip.close()

def download_video(video_url):
    try:
        print("Downloading video...")
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        block_size = 2048
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc='Video Download', position=0)

        with open(TEMP_VIDEO_PATH, "wb") as video_file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                video_file.write(data)

        progress_bar.close()

        video_duration = VideoFileClip(TEMP_VIDEO_PATH).duration
        print(f"Downloaded video duration is {video_duration} sec")
        if video_duration < 15:
            reversed_video_path = BASE_PATH + "reversed.mp4"
            reverse_and_append(TEMP_VIDEO_PATH, reversed_video_path)
            os.rename(reversed_video_path, TEMP_VIDEO_PATH)
        else:
            trimmed_video_path = BASE_PATH + "trimmer.mp4"
            adjust_video_length(TEMP_VIDEO_PATH, trimmed_video_path)
            os.rename(trimmed_video_path, TEMP_VIDEO_PATH)

        print("Video download completed.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error during video download: {e}")
        return False

def textsize(text, font):
    im = Image.new(mode="P", size=(0, 0))
    draw = ImageDraw.Draw(im)
    _, _, width, height = draw.textbbox((0, 0), text=text, font=font)
    return width, height

def add_text_to_frame(frame, text, font, video_dimensions, duration, max_duration):
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
        text_width, text_height = textsize(line, font)
        scale_factor = min(1.0, max_width / text_width)
        new_font_size = int(font.size * scale_factor)
        font_resized = ImageFont.truetype(font.path, new_font_size)
        text_width_resized, text_height_resized = textsize(line, font_resized)
        x_position = (video_dimensions[0] - text_width_resized) // 2
        draw.text((x_position, y_position), line, font=font_resized, fill=(255, 255, 255, 255))
        y_position += text_height_resized

        # Calculate the duration to display this line
        line_duration = (text_width / max_width) * (max_duration / len(lines))
        total_duration += line_duration

        # Check if the total duration exceeds the current video duration
        if total_duration >= duration:
            break

    return np.array(frame)

def crop_video(video_path, output_path, target_width, target_height):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = imageio.get_writer(output_path, fps=fps, macro_block_size=None)

    target_aspect_ratio = target_width / target_height
    original_aspect_ratio = original_width / original_height

    if target_aspect_ratio < original_aspect_ratio:
        crop_width = int(original_height * target_aspect_ratio)
        crop_start = (original_width - crop_width) // 2
        crop_end = crop_start + crop_width
    else:
        crop_width = original_width
        crop_start = 0
        crop_end = original_width

    with tqdm(total=frame_count, unit='frames', unit_scale=True, desc='Cropping Video', position=0) as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_cropped = cv2.resize(frame[:, crop_start:crop_end], (target_width, target_height))
            frame_resized = cv2.cvtColor(frame_cropped, cv2.COLOR_BGR2BGRA)

            out.append_data(frame_resized)
            pbar.update(1)

        out.close()
        cap.release()

    print("Video cropped successfully.")

def apply_blur(frame, blur_strength=2.0):
    return cv2.GaussianBlur(frame, (0, 0), blur_strength)

def apply_blur_to_video(video_path, output_path, blur_strength):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    out = imageio.get_writer(output_path, fps=fps, macro_block_size=None)

    with tqdm(total=frame_count, unit='frames', unit_scale=True, desc='Applying Blur', position=2) as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_with_blur = apply_blur(frame, blur_strength)

            out.append_data(frame_with_blur)
            pbar.update(1)

    out.close()
    cap.release()

def add_overlay(frame_pil):
    overlay = Image.new("RGBA", frame_pil.size, (0, 0, 0, int(255 * 0.4)))
    frame_pil = Image.alpha_composite(frame_pil.convert("RGBA"), overlay)

    return frame_pil.convert("RGB")

def process_cropped_video(video_path, quote, selected_font, max_duration=20.0):
    try:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        out = imageio.get_writer(os.path.join("./reels", generate_unique_filename("mp4")), fps=fps, macro_block_size=None)

        print("Processing video...")
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        font_size = min(int(original_height * 0.06), 80)
        font = ImageFont.truetype(selected_font, font_size)

        duration = 0.0

        with tqdm(total=frame_count, unit='frames', unit_scale=True, desc='Video Processing', position=1) as pbar:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                frame_pil = add_overlay(frame_pil)
                frame_with_text = add_text_to_frame(frame_pil, quote, font, (original_width, original_height), duration, max_duration)

                out.append_data(np.array(frame_with_text))
                duration += 1 / fps

                if duration >= max_duration:
                    break

                pbar.update(1)

        cap.release()
        out.close()

        print("Video processing completed.")
    except Exception as e:
        print(f"Error during video processing: {e}")
