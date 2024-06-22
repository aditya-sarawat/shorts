import requests
import re
from gpt4Free.runPrompt import runPrompt

def clean_text(input_text):
    pattern = r'"([^"]*)"'
    matches = re.findall(pattern, input_text)
    
    return matches[0]


def get_quote_from_ai(tags):
    try:
        quote_prompt = f"Generate a random motivational quote for a short video using the following tags: {tags}. Only return the quote, with no additional information."
        quote_response = runPrompt("Inspirational Quote Specialist", quote_prompt)
        quote = clean_text(quote_response)
        return quote
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during Quotable API request: {e}")
        return None
