import logging
import os
import random
import time
from pytube import YouTube
from pydub import AudioSegment
from youtubesearchpython import VideosSearch

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Destination folder for downloaded files
DESTINATION_FOLDER = "./motivational_content/__temp__"


def search_and_download_song(tags, max_retries=3, retry_delay=5):
    """
    Search YouTube for songs related to the provided tags, download one, and convert it to MP3 format.

    Args:
        tags (list): List of tags to search for.
        max_retries (int): Maximum number of download retries.
        retry_delay (int): Delay between download retries in seconds.
    """
    combined_results = []

    # Search YouTube for videos related to each tag
    for tag in tags:
        search_query = f"{tag} NoCopyrightSounds tune"
        videos_search = VideosSearch(search_query, limit=50)
        results = videos_search.result()["result"]

        # Filter results to include only those from the NoCopyrightSounds channel
        filtered_results = [
            result
            for result in results
            if result.get("channel")
            and result["channel"].get("name") == "NoCopyrightSounds"
        ]
        combined_results.extend(filtered_results)

    # If no relevant results are found, search for general NoCopyrightSounds videos
    if not combined_results and "NoCopyrightSounds" not in tags:
        search_query = "NoCopyrightSounds"
        videos_search = VideosSearch(search_query, limit=50)
        results = videos_search.result()["result"]

        # Filter results to include only those from the NoCopyrightSounds channel
        filtered_results = [
            result
            for result in results
            if result.get("channel")
            and result["channel"].get("name") == "NoCopyrightSounds"
        ]
        combined_results.extend(filtered_results)

    if not combined_results:
        logger.warning("No relevant videos found on YouTube.")
        return

    # Select a random video from the combined results
    selected_video = random.choice(combined_results)
    retries = 0

    # Attempt to download the selected video
    while retries < max_retries:
        try:
            video_url = f'https://www.youtube.com/watch?v={selected_video["id"]}'
            yt = YouTube(video_url)
            video = yt.streams.get_highest_resolution()

            # Create the destination folder if it doesn't exist
            os.makedirs(DESTINATION_FOLDER, exist_ok=True)

            # Download the video
            video.download(DESTINATION_FOLDER)

            # Convert the video to MP3 format
            video_path = os.path.join(DESTINATION_FOLDER, video.default_filename)
            audio = AudioSegment.from_file(video_path)
            mp3_path = os.path.join(DESTINATION_FOLDER, "audio.mp3")
            audio.export(mp3_path, format="mp3")

            # Remove the downloaded video file
            os.remove(video_path)

            logger.info("Song downloaded successfully.")
            return
        except Exception as e:
            retries += 1
            time.sleep(retry_delay)
            logger.error(f"Error downloading song: {e}")

    logger.error("Failed to download song after multiple retries.")
    return
