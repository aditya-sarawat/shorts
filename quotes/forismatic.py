import requests

def get_english_quote_from_forismatic():
    try:
        tags = get_tags_for_quote()
        response = requests.get(
            "http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en"
        )
        response.raise_for_status()
        quote_data = response.json()
        return quote_data["quoteText"]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Forismatic API request: {e}")
        return None