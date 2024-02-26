# motivational_content/quote_generator.py
import requests
import random

def get_tags_for_quote(language_choice):
    if (language_choice == 'english'):
        tags = ["education", "failure", "faith", "famous-quotes", "friendship", "generosity", "genius", "happiness", "imagination", "inspirational", "leadership", "love", "motivational", "opportunity", "power-quotes", "success", "time", "weakness"]
        num_tags_to_use = random.randint(1, 3)
        return random.sample(tags, num_tags_to_use)
    elif (language_choice == "hindi"):
        tags = ["success", "love", "attitude", "positive", "motivational"]
        return random.sample(tags , 1)

def get_english_quote(language_choice):
    try:
        tags = get_tags_for_quote(language_choice)
        tag_str = "|".join(tags)
        response = requests.get(f"https://api.quotable.io/random?tags={tag_str}")
        response.raise_for_status()
        quote_data = response.json()
        return tags, quote_data['content']
    except requests.exceptions.RequestException as e:
        print(f"Error during quotable API request: {e}")
        return None

def get_hindi_quote(language_choice):
    try:
        tags = get_tags_for_quote(language_choice)
        tag_str = "|".join(tags)
        response = requests.get(f"https://hindi-quotes.vercel.app/random/{tag_str}")
        response.raise_for_status()
        quote_data = response.json()
        return tags, quote_data['quote']
    except requests.exceptions.RequestException as e:
        print(f"Error during Hindi quote API request: {e}")
        return None
    
def get_motivational_quote_from_zenquotes():
    try:
        tags = ["inspirational", "failure", "faith", "leadership", "love", "motivational", "opportunity", "success", "time", "weakness"]
        response = requests.get("https://zenquotes.io/api/random")
        response.raise_for_status()
        quote_data = response.json()
        return tags, quote_data[0]['q']
    except requests.exceptions.RequestException as e:
        print(f"Error during Zenquotes API request: {e}")
        return None

def get_combined_quote():
    language_choice = random.choice(["english", "hindi"])

    if language_choice == "english":
        tags, quote = get_english_quote(language_choice) if random.randint(0, 10) > 5 else get_motivational_quote_from_zenquotes()
        return tags, quote, language_choice
    elif language_choice == "hindi":
        quote_type, quote = get_hindi_quote(language_choice)
        return quote_type, quote, language_choice
