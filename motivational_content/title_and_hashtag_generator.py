import random
import nltk

nltk.download("stopwords")
nltk.download("punkt")
from rake_nltk import Rake
import spacy


def extract_keywords(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    keywords = [
        token.text.lower() for token in doc if not token.is_stop and not token.is_punct
    ]
    return keywords


def extract_key_phrases(text):
    r = Rake()
    r.extract_keywords_from_text(text)
    key_phrases = r.get_ranked_phrases()
    return key_phrases


def get_title_and_hashtags(quote, tags=None):
    title = f"🔥 {quote} 🔥"
    keywords = extract_keywords(quote)
    key_phrases = extract_key_phrases(quote)
    if tags:
        keywords.extend([tag.lower() for tag in tags])

    relevant_terms = list(set(keywords + key_phrases))
    random.shuffle(relevant_terms)
    hashtags = [f"#{term}" for term in relevant_terms][:5]

    # update later
    hashtags = [
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
    for tag in tags:
        hashtags.append("#" + tag)

    return title, hashtags
