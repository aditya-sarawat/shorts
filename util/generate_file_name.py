import datetime
import random
import string
import os
import uuid
from util.logger import get_logger

logger = get_logger()


def generate_unique_filename(extension):
    try:
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        unique_id = uuid.uuid4().hex[
            :5
        ]  # Use first 5 characters of UUID for uniqueness
        return f"{current_datetime}_{unique_id}.{extension}"
    except Exception as e:
        logger.error(f"An error occurred while generating unique filename: {e}")
        return None
