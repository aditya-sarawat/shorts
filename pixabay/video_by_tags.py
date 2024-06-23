import os
import random
import requests
from dotenv import load_dotenv
from util.random import get_random
from util.logger import get_logger

logger = get_logger()

# Load environment variables
load_dotenv()

PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")


def get_top_videos(max_videos=200, tag=""):
    URL = f"https://pixabay.com/api/videos/?key={PIXABAY_API_KEY}&q={tag}&order=popular&per_page={max_videos}"

    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()

        # Check if any videos were found
        if "hits" in data:
            return data["hits"]
        else:
            logger.warning(f"No videos found on Pixabay for {tag} tag!")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Pixabay API request: {e}")
        return None


def get_random_video_by_tag(tags=[]):
    top_videos = []

    # Search for top videos for each tag and combine them
    for tag in tags:
        videos_for_tag = get_top_videos(200, tag)
        if videos_for_tag:
            top_videos.extend(videos_for_tag)

    if top_videos:
        random_video_hit = get_random(top_videos)
        video_url = random_video_hit["videos"]["large"]["url"]
        return video_url
    else:
        logger.warning("No videos found on Pixabay for the tags: {tags}")
        return None
