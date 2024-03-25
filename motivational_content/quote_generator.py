import requests
import random
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_tags_for_quote():
    """
    Get a random selection of tags for fetching a quote.
    :return: List of random tags.
    """
    tags = [
        "education",
        "failure",
        "faith",
        "famous-quotes",
        "friendship",
        "generosity",
        "genius",
        "happiness",
        "imagination",
        "inspirational",
        "leadership",
        "love",
        "motivational",
        "opportunity",
        "success",
        "time",
        "weakness",
        "power-quotes",
    ]
    num_tags_to_use = random.randint(1, 3)
    return random.sample(tags, num_tags_to_use)


def get_english_quote_from_forismatic():
    """
    Get an English quote from the Forismatic API.
    :return: Tags associated with the quote and the quote itself.
    """
    try:
        tags = get_tags_for_quote()
        response = requests.get(
            "http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en"
        )
        response.raise_for_status()
        quote_data = response.json()
        return tags, quote_data["quoteText"]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Forismatic API request: {e}")
        return None


def get_combined_quote():
    """
    Get a combined quote by fetching an English quote from the Forismatic API.
    :return: Tags associated with the quote and the quote itself.
    """
    tags, quote = get_english_quote_from_forismatic()
    return tags, quote
