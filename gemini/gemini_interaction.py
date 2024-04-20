import os
from util.logger import get_logger
from dotenv import load_dotenv
import google.generativeai as genai
from gemini.initiate_gemini import initiate_gemini_interaction

# Load environment variables from .env file
load_dotenv()

# Get logger
logger = get_logger()


def communicate_with_gemini(user_input):
    try:
        convo = initiate_gemini_interaction()  # Start Gemini chat session

        # Send user input to Gemini
        convo.send_message(user_input)
        response = convo.last.text  # Get response from Gemini

        info_message = f"Response from Gemini: {response}"
        logger.info(info_message)  # Log Gemini's response

        return response
    except Exception as e:
        error_message = f"Error: {e}"
        logger.error(error_message)  # Log any errors that occur
        return error_message
