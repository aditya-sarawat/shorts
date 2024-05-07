import requests
import random
from quotes.forismatic import get_english_quote_from_forismatic
from quotes.quotable import get_quote_from_quotable
from quotes.ai import get_quote_from_ai
from util.logger import get_logger

logger = get_logger()


def get_tags_for_quote():
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


def get_combined_quote():
    tags = get_tags_for_quote()
    # get_english_quote_from_forismatic
    quote_sources = [get_quote_from_quotable, get_quote_from_ai]
    random_source = random.choice(quote_sources)
    
    quote = random_source(tags)
    if quote:
        return tags, quote

    # If both APIs fail, return None
    return None
