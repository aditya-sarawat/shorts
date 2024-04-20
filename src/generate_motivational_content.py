import os
import random
import shutil
import logging

from quotes.quote import get_combined_quote
from util.check_dir import ensure_directory_exists
from util.delete_old_videos import delete_old_files
from util.download_video import download_video_by_url
from util.logger import get_logger
from util.metadata_for_videos import get_title_description_and_hashtags

from video_processor.add_blur_to_video import apply_blur_to_video
from video_processor.add_overlay_to_video import add_overlay_to_video
from video_processor.add_text_to_video import add_text_to_video
from video_processor.adjust_video_length import adjust_video_length_for_quote
from video_processor.combine_audio_video import combine_audio_video
from video_processor.crop_and_resize_video import crop_and_resize_video

from pixabay.animinated_video import get_random_animated_video
from pixabay.video_by_tags import get_random_video_by_tag

from youtube.download_video import download_video
from youtube.ncs import search_videos
from youtube.upload_shorts_on_yt import upload_to_youtube

logger = get_logger()

# Define constants
BASE_DIR = "./__temp__"
ENGLISH_FONTS_FOLDER = os.path.join("./fonts", "english")
VIDEO_PATHS = {
    "temp_video": os.path.join(BASE_DIR, "temp_video.mp4"),
    "cropped_video": os.path.join(BASE_DIR, "cropped_video.mp4"),
    "blurred_video": os.path.join(BASE_DIR, "blurred_video.mp4"),
    "overlay_video": os.path.join(BASE_DIR, "overlay_video.mp4"),
    "quote_video": os.path.join(BASE_DIR, "quote_video.mp4"),
    "audio": os.path.join(BASE_DIR, "audio.mp3"),
    "final_output_dir": "./reels",
}


def get_random_video_or_animated(tags):
    video_url = get_random_video_by_tag(tags) or get_random_animated_video()
    return video_url


def generate_quote_and_metadata():
    try:
        logger.info("Getting a quote and tags for the quote...")
        quote_info = get_combined_quote()
        if not quote_info:
            return None, None, None, None, None
        tags, quote = quote_info
        logger.info("Generating the Title and Hashtags for the video...")
        title, description, hashtags = get_title_description_and_hashtags(quote, tags)
        return tags, quote, title, description, hashtags
    except Exception as e:
        logger.error(f"An error occurred while generating quote and metadata: {e}")
        return None, None, None, None, None


def get_video_for_quote(tags, quote):
    try:
        logger.info("Downloading video for the quote...")
        for attempt in range(1, 6):
            video_url = get_random_video_or_animated(tags)
            if download_video_by_url(video_url):
                video_length, required_length = adjust_video_length_for_quote(
                    VIDEO_PATHS["temp_video"], quote
                )
                if video_length >= required_length:
                    return video_length
            logger.info("Video is smaller than required, retrying...")
        return None
    except Exception as e:
        logger.error(f"An error occurred while processing video: {e}")
        return None


def process_video(blur_strength, target_width, target_height, quote, video_length):
    selected_font = os.path.join(
        ENGLISH_FONTS_FOLDER, random.choice(os.listdir(ENGLISH_FONTS_FOLDER))
    )

    crop_and_resize_video(
        VIDEO_PATHS["temp_video"],
        VIDEO_PATHS["cropped_video"],
        target_width,
        target_height,
    )
    apply_blur_to_video(
        VIDEO_PATHS["cropped_video"], VIDEO_PATHS["blurred_video"], blur_strength
    )
    add_overlay_to_video(
        VIDEO_PATHS["blurred_video"],
        VIDEO_PATHS["overlay_video"],
    )
    add_text_to_video(
        VIDEO_PATHS["overlay_video"],
        VIDEO_PATHS["quote_video"],
        quote,
        selected_font,
        video_length,
    )


def generate_motivational_content():
    try:
        ensure_directory_exists(BASE_DIR)
        tags, quote, title, description, hashtags = generate_quote_and_metadata()
        if not tags or not quote:
            return None, None, None, None, None
        video_length = get_video_for_quote(tags, quote)
        if video_length == None:
            return None, None, None, None, None
        target_width, target_height = 720, 1280
        blur_strength = random.uniform(5, 10)

        process_video(blur_strength, target_width, target_height, quote, video_length)

        video_id = search_videos(tags)
        download_video(video_id, BASE_DIR)
        final_video_path = combine_audio_video(
            VIDEO_PATHS["audio"],
            VIDEO_PATHS["quote_video"],
            VIDEO_PATHS["final_output_dir"],
        )

        shutil.rmtree(BASE_DIR)

        if final_video_path and quote and title and description and hashtags:
            upload_to_youtube(final_video_path, quote, title, description, hashtags)
            logger.info(
                "Motivational content generation and YouTube upload completed successfully."
            )
        else:
            logger.error("Motivational content generation failed.")

    except Exception as e:
        logger.error(f"An error occurred during content generation: {e}")
        return None, None, None, None, None
