import logging
import time
from motivational_content.gemini import start_gemini_chat

# Default hashtags
DEFAULT_HASHTAGS = [
    "#shorts",
    "#youtubeshorts",
    "#youtube",
    "#short",
    "#shortvideo",
    "#trending",
    "#trendingshorts",
    "#quotes",
]

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

MAX_RETRIES = 5


def get_title_and_description_and_hashtags(quote, tags=None):
    """
    Generate a title, hashtags, and description for the YouTube Shorts video.
    :param quote: Input quote.
    :param tags: Optional list of tags.
    :return: Title, hashtags, and description.
    """
    retries = 0
    title = None
    final_hashtags = set()
    description = None

    while retries < MAX_RETRIES:
        try:
            # Generate title using Gemini
            title_prompt = f"Generate a fascinating one line title for a YouTube Shorts video featuring the quote: '{quote}'. Only return the title."
            title_response = start_gemini_chat(title_prompt)
            title = title_response.strip()

            # Ensure title includes '#shorts'
            if not any(hashtag.lower() == "#shorts" for hashtag in title.split()):
                title += " #shorts"

            # Generate description using Gemini
            description_prompt = f"Generate a accurate and catchy description for a YouTube Shorts video featuring the quote: '{quote}'. This description should provide a brief overview or teaser of what viewers can expect from the video. Only return the description."
            description_response = start_gemini_chat(description_prompt)
            description = (
                description_response.strip()
            )

            # Generate hashtags using Gemini
            prompt = f"Generate hashtags for a YouTube Shorts video to maximize views, aiming for it to reach the #1 trending spot. The video features the following quote: '{quote}', and the quote is generated using following tags: {tags}. Must include hashtags relevant to the quote's theme (e.g., motivational, funny, inspirational), considering current trends. Include a mix of general, quote-specific, and call-to-action hashtags. Also include the hashtags that are may not be relevant to the quote but are used to achieve the given target (e.g.. #TrendingNow, #Shorts, #YouTubeShorts). Only return the hashtags."

            response = start_gemini_chat(prompt)

            # Extract hashtags from the response
            hashtags = [word for word in response.split() if word.startswith("#")]

            if not hashtags:
                logger.info("No hashtags found in response. Retrying...")
                time.sleep(2)  # Adding a slight delay before retrying
                retries += 1
                continue

            # Add missing default hashtags
            final_hashtags = set(hashtags + DEFAULT_HASHTAGS)
            break  # Break out of the loop if successful
        except Exception as e:
            logger.error(f"Error generating title, description, and hashtags: {e}")
            retries += 1

    if not title:
        logger.info(
            "Max retries reached, returning default title, description, and hashtags."
        )
        title = "Default Title"
        description = "Default Description"

    return title, description, final_hashtags