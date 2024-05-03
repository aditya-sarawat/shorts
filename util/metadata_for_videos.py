import logging
import re
from gemini.gemini_interaction import communicate_with_gemini
from gpt4Free.runPrompt import runPrompt
from util.logger import get_logger

logger = get_logger()

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

ROLE = 'Famous Youtuber and Professional content creator'

def clean_text(text, phrases_to_remove=None):
    if phrases_to_remove is None:
        phrases_to_remove = ["**description:**", "description:", "title:", "**", ""]
    cleaned_text = text.strip()

    for phrase in phrases_to_remove:
        pattern = re.compile(re.escape(phrase), flags=re.IGNORECASE)
        cleaned_text = pattern.sub("", cleaned_text)

    if cleaned_text.startswith("**"):
        cleaned_text = cleaned_text[2:]

    if cleaned_text.endswith("**"):
        cleaned_text = cleaned_text[:-2]

    return cleaned_text.strip()


def generate_title(quote):
    title_prompt = f"Generate a fascinating one line title for a YouTube Shorts video featuring the quote: '{quote}'. Only return the title without any formatting, do not add '**Title:**' or any '**' or any thing like that, simply give me the title with no fancy editing"
    title_response = runPrompt(ROLE, title_prompt)
    title = clean_text(title_response)

    if not any(hashtag.lower() == "#Shorts" for hashtag in title.split()):
        title += " #Shorts  "

    return title


def generate_description(quote):
    description_prompt = f"Generate a accurate and catchy description for a YouTube Shorts video featuring the quote: '{quote}'. This description should provide a brief overview or teaser of what viewers can expect from the video and should be short and should not include hashtags. Only return the description without any formatting, do not add '**Description:**' or any '**' or any thing like that, simply give me the description with no fancy editing."
    description_response = runPrompt(ROLE, description_prompt)
    description = clean_text(description_response)

    return description


def generate_hashtags(quote, tags=None):
    prompt = f"Generate hashtags for a YouTube Shorts video to maximize views. The video features the following quote: '{quote}', and the quote is generated using following tags: {tags}. Must include hashtags relevant to the quote's theme (e.g., motivational, funny, inspirational), considering current trends. Include a mix of general, quote-specific, and call-to-action hashtags. Also include the hashtags that are may not be relevant to the quote but are used to achieve the given target (e.g.. #TrendingNow, #Shorts, #YouTubeShorts). Only return the hashtags without any formatting or additional information."

    response = runPrompt(ROLE, prompt)
    hashtags = [word for word in response.split() if word.startswith("#")]

    final_hashtags = set(hashtags + DEFAULT_HASHTAGS)

    return final_hashtags


def get_title_description_and_hashtags(quote, tags=None, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            title = generate_title(quote)
            description = generate_description(quote)
            hashtags = generate_hashtags(quote, tags)
            return title, description, hashtags
        except Exception as e:
            logger.error(f"Error generating title, description, and hashtags: {e}")
            retries += 1

    logger.warning(
        "Max retries reached."
    )
    return None
