import os
from util.logger import get_logger
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get logger
logger = get_logger()

# Get API key from environment variables
api_key = os.getenv("GENAI_API_KEY")
if not api_key:
    raise ValueError("GENAI_API_KEY environment variable is not set.")

genai.configure(api_key=api_key)

# Initialize conversation variable
convo = None


def initiate_gemini_interaction():
    global convo
    try:
        # Check if conversation has not been initialized
        if convo is None:
            # Configuration for model generation
            generation_config = {
                "temperature": 0.9,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 2048,
            }

            # Safety settings for filtering harmful content
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
            ]

            # Initialize the generative model
            model = genai.GenerativeModel(
                model_name="gemini-1.0-pro",
                generation_config=generation_config,
                safety_settings=safety_settings,
            )

            # Start the chat session
            convo = model.start_chat()

            # Log successful initialization of the chat
            logger.info("Gemini chat defined successfully!")

        return convo
    except Exception as e:
        # Log any errors that occur during initialization
        logger.error(f"Error: {e}")
        return f"Error: {e}"
