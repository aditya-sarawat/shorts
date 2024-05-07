import requests
import re
from gpt4Free.runPrompt import runPrompt

ROLE = "Famous Quote Writer"

def clean_text(input_text):
    pattern = r'"([^"]*)"'
    matches = re.findall(pattern, input_text)
    
    return matches[0]


def get_quote_from_ai(tags):
    try:
        quote_prompt = f"Generate or give a random quote that is related to '{tags}' tags. Only return the quote without any additional information"
        quote_response = runPrompt(ROLE, quote_prompt)
        quote = clean_text(quote_response)
        return quote
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Quotable API request: {e}")
        return None
