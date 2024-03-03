import os
import random
from motivational_content.pixabay_api import get_random_animated_video, get_random_video
from motivational_content.quote_generator import get_combined_quote
from motivational_content.video_processor import (
    download_video,
    check_and_process_video_for_quote,
    apply_blur_to_video,
    crop_and_resize_video,
    process_cropped_video,
)

fonts_folder = "./fonts"
hindi_fonts_folder = os.path.join(fonts_folder, "hindi")
english_fonts_folder = os.path.join(fonts_folder, "english")

BASE_DIR = "./motivational_content/__temp__"


def generate_motivational_content():
    quote_info = get_combined_quote()
    if not quote_info:
        print("No quote found.")
        print("Unable to create short!!")
        return

    tags, quote, language = quote_info
    print(f"Tags: {tags}")
    print(f"Quote: {quote}")
    print(f"Language: {language}")

    video_url = get_random_video(tags) or get_random_animated_video()

    if not video_url:
        print("No video found.")
        print("Unable to create short!!")
        return

    available_fonts_folder = (
        hindi_fonts_folder if language == "hindi" else english_fonts_folder
    )
    available_fonts = [
        f for f in os.listdir(available_fonts_folder) if f.endswith(".ttf")
    ]

    if not available_fonts:
        print("No available fonts found.")
        print("Unable to create short!!")
        return

    selected_font = os.path.join(available_fonts_folder, random.choice(available_fonts))

    if not download_video(video_url):
        return

    try:
        TEMP_VIDEO_PATH = os.path.join(BASE_DIR, "temp_video.mp4")
        CROPPED_VIDEO_PATH = os.path.join(BASE_DIR, "cropped_video.mp4")
        BLURRED_VIDEO_PATH = os.path.join(BASE_DIR, "blurred_video.mp4")

        video_length = check_and_process_video_for_quote(TEMP_VIDEO_PATH, quote)
        target_width, target_height = 720, 1280
        blur_strength = random.uniform(5, 10)
        print(f"Blur strength: {blur_strength}")

        crop_and_resize_video(
            TEMP_VIDEO_PATH, CROPPED_VIDEO_PATH, target_width, target_height
        )
        apply_blur_to_video(CROPPED_VIDEO_PATH, BLURRED_VIDEO_PATH, blur_strength)
        process_cropped_video(BLURRED_VIDEO_PATH, quote, selected_font, video_length)

    finally:
        for file_path in [TEMP_VIDEO_PATH, CROPPED_VIDEO_PATH, BLURRED_VIDEO_PATH]:
            if os.path.exists(file_path):
                os.remove(file_path)


generate_motivational_content()
