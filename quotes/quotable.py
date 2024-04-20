import requests

def get_quote_from_quotable(tags):
    try:
        formatted_tags = '|'.join(tags)
        response = requests.get(f"https://api.quotable.io/random?tags={formatted_tags}")
        response.raise_for_status()
        quote_data = response.json()
        return quote_data["content"]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Quotable API request: {e}")
        return None