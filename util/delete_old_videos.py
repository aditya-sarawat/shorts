import datetime
import random
import string
import os
import uuid
from util.logger import get_logger

logger = get_logger()


def delete_old_files(folder_path, days_threshold=4):
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
