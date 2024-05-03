from g4f.client import Client
import os
from util.logger import get_logger

# Get logger
logger = get_logger()


def runPrompt(role, prompt):
    try:
        client = Client()

        # Define the message for the GPT-4 model
        message = {"role": role, "content": prompt}

        # Call GPT-4 to generate completion
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[message],
        )

        # Return the generated completion
        completion_content = response.choices[0].message.content

        # Log the successful completion
        logger.info("Prompt executed successfully.")
        print(completion_content)

        return completion_content
    except Exception as e:
        # Log any errors that occur during prompt execution
        logger.error(f"Error: {e}")
        return f"Error: {e}"
