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
    title_prompt = f"Generate a catchy title for a short video based on the quote: {quote}"
    title_response = runPrompt("Quote-to-Title Specialist", title_prompt)
    title = clean_text(title_response)

    if not any(hashtag.lower() == "#Shorts" for hashtag in title.split()):
        title += " #Shorts  "

    return title


def generate_description(quote):
    description_prompt = f"Create a concise description for a short video based on the quote: {quote}"
    description_response = runPrompt("Creative Video Synopsis Writer", description_prompt)
    description = clean_text(description_response)

    return description


def generate_hashtags(quote, tags=None):
    prompt = f"Generate relevant hashtags for a short video based on the quote: {quote}. Incorporate the tags {tags} used to generate the quote."

    hashtags_response = runPrompt("Social Media Engagement Specialist", prompt)
    hashtags = [word for word in hashtags_response.split() if word.startswith("#")]
    
    for default_tag in DEFAULT_HASHTAGS:
        if default_tag not in hashtags:
            hashtags.append(default_tag)

    return hashtags


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
