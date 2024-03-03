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
TEMP_VIDEO_PATH = os.path.join(BASE_DIR, "temp_video.mp4")
CROPPED_VIDEO_PATH = os.path.join(BASE_DIR, "cropped_video.mp4")
BLURRED_VIDEO_PATH = os.path.join(BASE_DIR, "blurred_video.mp4")


def get_random_video_or_animated(tags):
    video_url = get_random_video(tags)
    if not video_url:
        video_url = get_random_animated_video()
    return video_url


def generate_motivational_content():
    quote_info = get_combined_quote()
    if not quote_info:
        print("No quote found. Unable to create short!!")
        return

    tags, quote, language = quote_info
    print(f"Tags: {tags}\nQuote: {quote}\nLanguage: {language}")

    attempt_limit = 3
    for attempt in range(1, attempt_limit + 1):
        print(f"Attempt {attempt}/{attempt_limit}")

        video_url = get_random_video_or_animated(tags)
        if not video_url:
            print("No video found. Unable to create short!!")
            return

        available_fonts_folder = (
            hindi_fonts_folder if language == "hindi" else english_fonts_folder
        )
        available_fonts = [
            f for f in os.listdir(available_fonts_folder) if f.endswith(".ttf")
        ]

        if not available_fonts:
            print("No available fonts found. Unable to create short!!")
            return

        selected_font = os.path.join(
            available_fonts_folder, random.choice(available_fonts)
        )

        if not download_video(video_url):
            print("No video available. Unable to create short!!")
            return

        try:
            video_length, required_length = check_and_process_video_for_quote(
                TEMP_VIDEO_PATH, quote
            )
            print(f"Video length: {video_length}, Required length: {required_length}")
            if video_length >= required_length:
                break
            else:
                print(
                    f"Attempt {attempt}/{attempt_limit}: Video length is not sufficient. Retrying..."
                )

        except Exception as e:
            print(f"Error processing video: {e}")
            return

    else:
        print(f"Failed after {attempt_limit} attempts. Unable to create short!!")
        return

    print("\n\n")
    print(f"Video length: {video_length}, Required length: {required_length}")

    target_width, target_height = 720, 1280
    blur_strength = random.uniform(5, 10)
    print(f"Blur strength: {blur_strength}")

    crop_and_resize_video(
        TEMP_VIDEO_PATH, CROPPED_VIDEO_PATH, target_width, target_height
    )
    apply_blur_to_video(CROPPED_VIDEO_PATH, BLURRED_VIDEO_PATH, blur_strength)
    process_cropped_video(BLURRED_VIDEO_PATH, quote, selected_font, video_length)

    for file_path in [TEMP_VIDEO_PATH, CROPPED_VIDEO_PATH, BLURRED_VIDEO_PATH]:
        if os.path.exists(file_path):
            os.remove(file_path)


generate_motivational_content()
