import random
import nltk
from rake_nltk import Rake
import spacy
import logging

# Download NLTK resources
nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)

# Default hashtags
DEFAULT_HASHTAGS = [
    "#shorts",
    "#youtubeshorts",
    "#youtube",
    "#short",
    "#shortvideo",
    "#trending",
    "#trendingshorts",
    "#motivational",
    "#motivation",
    "#quotes",
    "#memes",
    "#life",
]

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def extract_keywords(text):
    """
    Extract keywords from the given text using SpaCy.
    :param text: Input text.
    :return: List of keywords.
    """
    try:
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        keywords = [
            token.text.lower()
            for token in doc
            if not token.is_stop and not token.is_punct
        ]
        return keywords
    except Exception as e:
        logger.error(f"Error extracting keywords: {e}")
        return []


def extract_key_phrases(text):
    """
    Extract key phrases from the given text using RAKE.
    :param text: Input text.
    :return: List of key phrases.
    """
    try:
        r = Rake()
        r.extract_keywords_from_text(text)
        key_phrases = r.get_ranked_phrases()
        return key_phrases
    except Exception as e:
        logger.error(f"Error extracting key phrases: {e}")
        return []


def get_title_and_hashtags(quote, tags=None):
    """
    Generate a title and hashtags for the quote.
    :param quote: Input quote.
    :param tags: Optional list of tags.
    :return: Title and hashtags.
    """
    try:
        title = f"🔥 {quote} 🔥"
        keywords = extract_keywords(quote)
        key_phrases = extract_key_phrases(quote)

        # Combine keywords and key phrases
        relevant_terms = list(set(keywords + key_phrases))
        random.shuffle(relevant_terms)
        hashtag_terms = relevant_terms[:5]

        # Generate hashtags from relevant terms
        hashtags = [f"#{term}" for term in hashtag_terms]

        # Add default hashtags
        final_hashtags = DEFAULT_HASHTAGS + hashtags

        # Add user-defined tags as hashtags
        if tags:
            for tag in tags:
                final_hashtags.append("#" + tag)

        return title, final_hashtags
    except Exception as e:
        logger.error(f"Error generating title and hashtags: {e}")
        return None, []
