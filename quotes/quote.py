import requests
import random
from quotes.forismatic import get_english_quote_from_forismatic
from quotes.quotable import get_quote_from_quotable
from quotes.ai import get_quote_from_ai
from util.logger import get_logger

logger = get_logger()

quotable_tags = [
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

motivational_tags = [
    "Achieve",
    "Achievement",
    "Ambition",
    "Balance",
    "Believe",
    "Bravery",
    "Clarity",
    "Confidence",
    "Courage",
    "Dedication",
    "Determination",
    "Dreams",
    "Drive",
    "Empower",
    "Empowerment",
    "Encouragement",
    "Fearless",
    "Focus",
    "Goals",
    "Gratitude",
    "GrowthMindset",
    "HardWork",
    "Hope",
    "Inspiration",
    "InspirationDaily",
    "Inspire",
    "Innovation",
    "InnerStrength",
    "Leadership",
    "Mindfulness",
    "Mindset",
    "Motivate",
    "MotivationalMindset",
    "MotivationalQuotes",
    "Motivation",
    "NeverGiveUp",
    "NewBeginnings",
    "Overcome",
    "Passion",
    "Perseverance",
    "PersonalGrowth",
    "PositiveChange",
    "PositiveThinking",
    "PositiveVibes",
    "Positivity",
    "Possibilities",
    "Potential",
    "Purpose",
    "Resilience",
    "SelfBelief",
    "SelfCare",
    "SelfImprovement",
    "SelfLove",
    "Strength",
    "StrengthInAdversity",
    "Success",
    "SuccessMindset",
    "SuccessStories",
    "Transformation",
    "Triumph",
    "Uplift",
    "Vision",
    "Wellbeing",
    "Wellness",
    "Wisdom",
]


def get_tags_for_quote(tag_list):
    num_tags_to_use = random.randint(1, 3)
    return random.sample(tag_list, num_tags_to_use)


def get_combined_quote():
    quote_sources = [get_quote_from_ai]
    random_source = random.choice(quote_sources)

    if random_source == get_quote_from_quotable:
        tags = get_tags_for_quote(quotable_tags)
    else:
        tags = get_tags_for_quote(motivational_tags)

    quote = random_source(tags)

    if quote:
        return tags, quote

    return None
