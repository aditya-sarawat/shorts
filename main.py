import logging
from motivational_content import generate_motivational_content
from upload_shorts_on_yt import upload_to_youtube

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        # Generate motivational content
        video_path, quote, title, description, hashtags = generate_motivational_content()

        # Upload the generated content to YouTube
        upload_to_youtube(video_path, quote, title, description, hashtags)

        logger.info(
            "Motivational content generation and YouTube upload completed successfully."
        )
    except Exception as e:
        logger.error(f"An error occurred: {e}")
