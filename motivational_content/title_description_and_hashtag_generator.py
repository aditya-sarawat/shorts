import logging
import time
import re
from motivational_content.gemini import start_gemini_chat

# Default hashtags
DEFAULT_HASHTAGS = [
    "#Shorts",
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


def clean_text(
    text, phrases_to_remove=["**description:**", "description:", "title:", "**", ""]
):
    """
    This function removes unwanted phrases from a text string.

    Args:
        text: The text string to clean.
        phrases_to_remove: A list of phrases to remove from the text.

    Returns:
        The cleaned text string.
    """
    cleaned_text = text.strip()

    # Remove all occurrences of phrases (case-insensitive)
    for phrase in phrases_to_remove:
        # Compile the phrase as a case-insensitive regular expression
        pattern = re.compile(re.escape(phrase), flags=re.IGNORECASE)
        cleaned_text = pattern.sub("", cleaned_text)

    # Remove leading double asterisks
    if cleaned_text.startswith("**"):
        cleaned_text = cleaned_text[2:]

    # Remove trailing double asterisks
    if cleaned_text.endswith("**"):
        cleaned_text = cleaned_text[:-2]

    return cleaned_text.strip()


def get_title_and_description_and_hashtags(quote, tags=None):
    """
    Generate a title, hashtags, and description for the YouTube Shorts video.

    Args:
        quote: Input quote.
        tags: Optional list of tags.

    Returns:
        Title, description, and hashtags.
    """
    retries = 0
    title = None
    final_hashtags = set()
    description = None

    while retries < MAX_RETRIES:
        try:
            # Generate title using Gemini
            title_prompt = f"Generate a fascinating one line title for a YouTube Shorts video featuring the quote: '{quote}'. Only return the title without any formatting, do not add '**Title:**' or any '**' or any thing like that, simply give me the title with no fancy editing"
            title_response = start_gemini_chat(title_prompt)
            title = clean_text(title_response)  # Remove unwanted phrases from title

            # Ensure title includes '#shorts'
            if not any(hashtag.lower() == "#Shorts" for hashtag in title.split()):
                title += " #Shorts  "

            # Generate description using Gemini
            description_prompt = f"Generate a accurate and catchy description for a YouTube Shorts video featuring the quote: '{quote}'. This description should provide a brief overview or teaser of what viewers can expect from the video and should be short and should not include hashtags. Only return the description without any formatting, do not add '**Description:**' or any '**' or any thing like that, simply give me the description with no fancy editing."
            description_response = start_gemini_chat(description_prompt)
            description = clean_text(
                description_response
            )  # Remove unwanted phrases from description

            # Generate hashtags using Gemini
            prompt = f"Generate hashtags for a YouTube Shorts video to maximize views. The video features the following quote: '{quote}', and the quote is generated using following tags: {tags}. Must include hashtags relevant to the quote's theme (e.g., motivational, funny, inspirational), considering current trends. Include a mix of general, quote-specific, and call-to-action hashtags. Also include the hashtags that are may not be relevant to the quote but are used to achieve the given target (e.g.. #TrendingNow, #Shorts, #YouTubeShorts). Only return the hashtags without any formatting or additional information."

            response = start_gemini_chat(prompt)

            # Extract hashtags from the response
            hashtags = [word for word in response.split() if word.startswith("#")]

            if not hashtags:
                logger.info("No hashtags found in response. Retrying...")
                time.sleep(2)
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
