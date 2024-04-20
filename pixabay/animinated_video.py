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


def get_top_animated_videos(max_videos=200):
    URL = f"https://pixabay.com/api/videos/?key={PIXABAY_API_KEY}&order=popular&video_type=animation&per_page={max_videos}"

    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()

        if "hits" in data:
            return data["hits"]
        else:
            logger.warning("No animated videos found on Pixabay")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Pixabay API request: {e}")
        return None


def get_random_animated_video():
    top_animated_videos = get_top_animated_videos(200)

    if top_animated_videos:
        random_video_hit = get_random(top_animated_videos)
        video_url = random_video_hit["videos"]["large"]["url"]
        return video_url
    else:
        logger.warning("No animated videos found on Pixabay.")
        return None
