# motivational_content/quote_generator.py
import requests
import random


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
        "power-quotes"
    ]
    num_tags_to_use = random.randint(1, 3)
    return random.sample(tags, num_tags_to_use)


def get_motivational_quote_from_quorable():
    try:
        tags = get_tags_for_quote()
        tag_str = "|".join(tags)
        response = requests.get(f"https://api.quotable.io/random?tags={tag_str}")
        response.raise_for_status()
        quote_data = response.json()
        return tags, quote_data["content"]
    except requests.exceptions.RequestException as e:
        print(f"Error during quotable API request: {e}")
        return None


def get_motivational_quote_from_zenquotes():
    try:
        tags = [
            "inspirational",
            "failure",
            "faith",
            "leadership",
            "love",
            "motivational",
            "opportunity",
            "success",
            "time",
            "weakness",
        ]
        response = requests.get("https://zenquotes.io/api/random")
        response.raise_for_status()
        quote_data = response.json()
        return tags, quote_data[0]["q"]
    except requests.exceptions.RequestException as e:
        print(f"Error during Zenquotes API request: {e}")
        return None


def get_english_quote_from_forismatic():
    try:
        tags = get_tags_for_quote()
        response = requests.get(
            "http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en"
        )
        response.raise_for_status()
        quote_data = response.json()
        return tags, quote_data["quoteText"]
    except requests.exceptions.RequestException as e:
        print(f"Error during Forismatic API request: {e}")
        return None


def get_english_quote_from_quotefancy():
    try:
        tags = get_tags_for_quote()
        response = requests.get("https://api.quotefancy.com/quotes/")
        response.raise_for_status()
        quote_data = response.json()
        random_quote = random.choice(quote_data)
        return tags, random_quote["quote"]
    except requests.exceptions.RequestException as e:
        print(f"Error during QuoteFancy API request: {e}")
        return None


def get_combined_quote():
    random_number = random.randint(0, 10)

    # if random_number <= 2:
    #     tags, quote = get_motivational_quote_from_quorable()
    # elif random_number <= 5:
    #     tags, quote = get_motivational_quote_from_zenquotes()
    # elif random_number <= 8:
    #     tags, quote = get_english_quote_from_quotefancy()
    # else:
    #     tags, quote = get_english_quote_from_forismatic()

    tags, quote = get_english_quote_from_forismatic()
    return tags, quote
