import os
import random
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")


def get_random_video_url(video_hits):
    """
    Get a random video URL from the provided list of video hits.
    :param video_hits: List of video hits.
    :return: Random video URL.
    """
    if video_hits:
        random_video_hit = random.choice(video_hits)
        video_url = random_video_hit["videos"]["large"]["url"]
        return video_url
    else:
        return None


def get_top_videos_by_tags(max_videos=200, tag=""):
    """
    Get top videos from Pixabay API based on a specific tag.
    :param max_videos: Maximum number of videos to retrieve.
    :param tag: Tag to search for.
    :return: List of top video hits.
    """
    URL = f"https://pixabay.com/api/videos/?key={PIXABAY_API_KEY}&q={tag}&order=popular&per_page={max_videos}"

    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()

        if int(data["total"]) > 0:
            return data["hits"]
        else:
            logger.warning(f"No videos found on Pixabay for {tag} tag!")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Pixabay API request: {e}")
        return None


def get_top_animated_videos(max_videos=200):
    """
    Get top animated videos from Pixabay API.
    :param max_videos: Maximum number of videos to retrieve.
    :return: List of top animated video hits.
    """
    URL = f"https://pixabay.com/api/videos/?key={PIXABAY_API_KEY}&order=popular&video_type=animation&per_page={max_videos}"

    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()

        if int(data["total"]) > 0:
            return data["hits"]
        else:
            logger.warning("No animated videos found on Pixabay")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Pixabay API request: {e}")
        return None


def get_random_video(tags=[]):
    """
    Get a random video URL based on provided tags.
    :param tags: List of tags to search for.
    :return: Random video URL.
    """
    top_videos = []

    # Search for top videos for each tag and combine them
    for tag in tags:
        videos_for_tag = get_top_videos_by_tags(200, tag)
        if videos_for_tag:
            top_videos.extend(videos_for_tag)

    if top_videos:
        video_url = get_random_video_url(top_videos)
        return video_url
    else:
        logger.warning("No videos found on Pixabay.")
        return None


def get_random_animated_video():
    """
    Get a random animated video URL from Pixabay.
    :return: Random animated video URL.
    """
    top_animated_videos = get_top_animated_videos(200)

    if top_animated_videos:
        video_url = get_random_video_url(top_animated_videos)
        return video_url
    else:
        logger.warning("No animated videos found on Pixabay.")
        return None
