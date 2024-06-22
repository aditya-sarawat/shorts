from g4f.client import Client
import os
from util.logger import get_logger

# Get logger
logger = get_logger()


def runPrompt(role, prompt):
    try:
        client = Client()

        # Define the message for the GPT-3.5-turbo model
        message = {"role": role, "content": prompt}

        # Call GPT-3.5-turbo to generate completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[message],
        )

        # Return the generated completion
        completion_content = response.choices[0].message.content

        # Log the successful completion
        logger.info("Prompt executed successfully.")

        return completion_content
    except Exception as e:
        # Log any errors that occur during prompt execution
        logger.error(f"Error: {e}")
        return f"Error: {e}"
