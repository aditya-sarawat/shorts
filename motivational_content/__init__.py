import logging
import os
import random
import shutil
from motivational_content.ncs_youtube import search_and_download_song
from motivational_content.pixabay_api import get_random_animated_video, get_random_video
from motivational_content.quote_generator import get_combined_quote
from motivational_content.title_description_and_hashtag_generator import get_title_and_description_and_hashtags
from motivational_content.video_processor import (
    download_video,
    check_and_process_video_for_quote,
    apply_blur_to_video,
    crop_and_resize_video,
    process_cropped_video,
    combine_audio_video,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Define the path for English fonts
english_fonts_folder = os.path.join("./fonts", "english")

# Define the base directory for temporary files
base_dir = "./motivational_content/__temp__"
# Define paths for temporary video files
video_paths = {
    "temp_video": os.path.join(base_dir, "temp_video.mp4"),
    "cropped_video": os.path.join(base_dir, "cropped_video.mp4"),
    "blurred_video": os.path.join(base_dir, "blurred_video.mp4"),
    "quote_video": os.path.join(base_dir, "quote_video.mp4"),
    "audio": os.path.join(base_dir, "audio.mp3"),
}


def get_random_video_or_animated(tags):
    """
    Get a random video from Pixabay API based on provided tags.
    If no video found, get a random animated video instead.
    """
    video_url = get_random_video(tags) or get_random_animated_video()
    return video_url


def generate_motivational_content():
    """
    Generate motivational content by combining a random video with a quote.
    """
    try:
        # Create the __temp__ directory if it doesn't exist
        os.makedirs(base_dir, exist_ok=True)

        # Retrieve a combined quote to use in the content generation
        logger.info("Getting a quote and tags for the quote...")
        quote_info = get_combined_quote()
        if not quote_info:
            return

        # Extract tags and quote from the retrieved quote information
        tags, quote = quote_info
        # Generate title and hashtags based on the quote and tags
        logger.info("Generating the Title and Hashtags for the video...")
        title, description, hashtags = get_title_and_description_and_hashtags(quote, tags)

        # Check available fonts for text overlay on the video
        logger.info("Checking for the available fonts and selecting the random available font...")
        available_fonts = [
            f for f in os.listdir(english_fonts_folder) if f.endswith(".ttf")
        ]

        if not available_fonts:
            return
        
        selected_font = os.path.join(
            english_fonts_folder, random.choice(available_fonts)
        )

        # Attempt to find a suitable video to accompany the quote
        logger.info("Downloading video for the quote...")
        attempt_limit = 5
        for attempt in range(1, attempt_limit + 1):
            video_url = get_random_video_or_animated(tags)
            if not video_url:
                return

            # Download the selected video
            if not download_video(video_url):
                return

            try:
                # Check and process the video to determine its suitability for the quote
                video_length, required_length = check_and_process_video_for_quote(
                    video_paths["temp_video"], quote
                )
                if video_length >= required_length:
                    break
                else:
                    logger.info("Video length is less than required length, retrying...")

            except Exception as e:
                return

        else:
            return
        
        # Set target dimensions and blur strength for video processing
        target_width, target_height = 720, 1280
        blur_strength = random.uniform(5, 10)

        # Crop and resize the video
        logger.info("Cropping video for youtube shorts and insatagram reel...")
        crop_and_resize_video(
            video_paths["temp_video"],
            video_paths["cropped_video"],
            target_width,
            target_height,
        )

        # Apply blur effect to the video
        logger.info("Applying blur to the cropped video...")
        apply_blur_to_video(
            video_paths["cropped_video"], video_paths["blurred_video"], blur_strength
        )

        # Process the video with text overlay
        logger.info("Adding quote to the blurred video...")
        process_cropped_video(
            video_paths["blurred_video"], quote, selected_font, video_length
        )

        # Search and download background music for the video
        logger.info("Downloading the Copyright Free Sound for video...")
        search_and_download_song(tags)

        # Combine audio and video to produce the final motivational content
        logger.info("Adding song to the quote video...")
        final_video_path = combine_audio_video(
            video_paths["audio"], video_paths["quote_video"]
        )

        # Remove the entire __temp__ directory and its contents
        shutil.rmtree(base_dir)

        return final_video_path, quote, title, description, hashtags
    except Exception as e:
        logger.error(f"An error occurred during content generation: {e}")
        return None, None, None, None, None
