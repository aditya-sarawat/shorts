import os
import random
from motivational_content.pixabay_api import get_random_animated_video, get_random_video
from motivational_content.quote_generator import get_combined_quote
from motivational_content.video_processor import download_video, check_and_process_video_for_quote, apply_blur_to_video, crop_video, process_cropped_video

fonts_folder = "./fonts"
hindi_fonts_folder = os.path.join(fonts_folder, "hindi")
english_fonts_folder = os.path.join(fonts_folder, "english")

BASE_DIR = "./motivational_content/__temp__"
CROPPED_VIDEO_PATH = os.path.join(BASE_DIR, "cropped_video.mp4")
TEMP_VIDEO_PATH = os.path.join(BASE_DIR, "temp_video.mp4")
BLURRED_VIDEO_PATH = os.path.join(BASE_DIR, "blurred_video.mp4")

def generate_motivational_content():
    quote_info = get_combined_quote()
    if quote_info:
        tags, quote, language = quote_info
        print(f"Tags: {tags}")
        print(f"Quote: {quote}")
        print(f"Language: {language}")

        video_url = get_random_video(tags)

        if video_url is None:
            print("No videos found on Pixabay using tags, fetching random animinated video!")
            video_url = get_random_animated_video()

        if video_url:
            if language == 'english':
                available_fonts = [f for f in os.listdir(english_fonts_folder) if f.endswith('.ttf')] 
            elif language == "hindi":
                available_fonts = [f for f in os.listdir(hindi_fonts_folder) if f.endswith('.ttf')]
                

            if not available_fonts:
                print("No available fonts found.")
                print("Unable to create short!!")
                return

            selected_font = os.path.join(hindi_fonts_folder if language == "hindi" else english_fonts_folder, random.choice(available_fonts))

            if download_video(video_url):
                video_length = check_and_process_video_for_quote(TEMP_VIDEO_PATH, quote)
                target_width = 720
                target_height = 1280

                blur_strength = random.uniform(5, 10)
                print(f"Blur strength: {blur_strength}")

                crop_video(TEMP_VIDEO_PATH, CROPPED_VIDEO_PATH, target_width, target_height)
                apply_blur_to_video(CROPPED_VIDEO_PATH, BLURRED_VIDEO_PATH, blur_strength)
                process_cropped_video(BLURRED_VIDEO_PATH, quote, selected_font, video_length)
                
                os.remove(TEMP_VIDEO_PATH)
                os.remove(CROPPED_VIDEO_PATH)
                os.remove(BLURRED_VIDEO_PATH)
        else:
            print("No video found.")
            print("Unable to create short!!")
            return
    else:
        print("No quote found.")
        print("Unable to create short!!")
        return
