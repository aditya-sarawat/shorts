import logging
import datetime
import random
import string

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
