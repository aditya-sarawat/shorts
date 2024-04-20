import os
import requests
from tqdm import tqdm
from util.logger import get_logger
from util.check_dir import ensure_directory_exists

logger = get_logger()

# Base directory
BASE_PATH = "./__temp__/"
TEMP_VIDEO_PATH = os.path.join(BASE_PATH, "temp_video.mp4")


def download_video_by_url(video_url):
    try:
        ensure_directory_exists(TEMP_VIDEO_PATH)
        response = requests.get(video_url, stream=True)
        response.raise_for_status()

        with open(TEMP_VIDEO_PATH, "wb") as video_file:
            for data in response.iter_content(chunk_size=8192):
                video_file.write(data)

        logger.info("Video downloaded successfully.")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Error downloading video: {e}")
        return False
