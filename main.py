from src.generate_motivational_content import generate_motivational_content
from util.logger import get_logger

logger = get_logger()

if __name__ == "__main__":
    try:
        generate_motivational_content()

    except Exception as e:
        logger.error(f"An error occurred: {e}")
