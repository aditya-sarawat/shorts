import os
import random
import time
from pytube import YouTube
from pydub import AudioSegment
from youtubesearchpython import VideosSearch
from util.check_dir import ensure_directory_exists
from util.logger import get_logger

logger = get_logger()


def download_video(video_id, destination_folder, max_retries=3, retry_delay=5):
    ensure_directory_exists(destination_folder)
    retries = 0

    while retries < max_retries:
        try:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            yt = YouTube(video_url)
            video = yt.streams.get_highest_resolution()

            # Download video
            video.download(destination_folder)

            # Convert video to audio (mp3)
            video_path = os.path.join(destination_folder, video.default_filename)
            audio = AudioSegment.from_file(video_path)
            mp3_path = os.path.join(destination_folder, "audio.mp3")
            audio.export(mp3_path, format="mp3")

            # Remove the downloaded video file
            os.remove(video_path)

            logger.info("Video downloaded from YouTube successfully.")
            return mp3_path
        except Exception as e:
            retries += 1
            time.sleep(retry_delay)
            logger.error(f"Error downloading song: {e}")

    logger.error("Failed to download video from YouTube after multiple retries.")
    return None
