import os
import logging
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Read the API key from the environment
api_key = os.getenv("GENAI_API_KEY")
genai.configure(api_key=api_key)


def start_gemini_chat(user_input):
    try:
        # Set up the model
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

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

        model = genai.GenerativeModel(
            model_name="gemini-1.0-pro",
            generation_config=generation_config,
            safety_settings=safety_settings,
        )

        # Start the chat
        convo = model.start_chat(
            history=[
                {"role": "user", "parts": [user_input]},
                {
                    "role": "model",
                    "parts": [
                        "I'm here and ready for testing! What would you like me to do? \n\nI can answer questions, generate different creative text formats, translate languages, and more. Just let me know what you have in mind."
                    ],
                },
            ]
        )

        # Send user input and get response
        convo.send_message(user_input)
        response = convo.last.text

        # Log the response
        logger.info("Response from Gemini: %s", response)

        return response
    except Exception as e:
        logger.error("Error encountered: %s", e)
        return f"Error: {e}"
