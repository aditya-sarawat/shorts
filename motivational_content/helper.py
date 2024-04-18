import logging
import datetime
import random
import string
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def generate_unique_filename(extension):
    """
    Generate a unique filename using the current datetime and a random suffix.

    Args:
        extension (str): File extension to be appended to the filename.

    Returns:
        str: Unique filename string.
    """
    try:
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        random_suffix = "".join(
            random.choices(string.ascii_letters + string.digits, k=5)
        )
        return f"{current_datetime}_{random_suffix}.{extension}"
    except Exception as e:
        logger.error(f"An error occurred while generating unique filename: {e}")
        return None


def delete_old_files(folder_path, days_threshold=4):
    """
    Delete files older than a specified number of days from a folder.

    Args:
        folder_path (str): Path to the folder.
        days_threshold (int): Number of days. Files older than this will be deleted.
    """
    try:
        # Get the current datetime
        current_datetime = datetime.datetime.now()

        # Iterate over the files in the folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            
            # Get the creation time of the file
            creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
            
            # Calculate the difference in days
            days_difference = (current_datetime - creation_time).days
            
            # If the file is older than the threshold, delete it
            if days_difference > days_threshold:
                os.remove(file_path)
                logger.info(f"Deleted file: {file_path}")
    except Exception as e:
        logger.info(f"An error occurred while deleting old files: {e}")
