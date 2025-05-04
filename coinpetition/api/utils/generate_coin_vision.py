"""
Utility to generate a vision statement for a coin using Google Gemini API.
"""

import google.generativeai as genai
from typing import Dict

import os

API_KEY = os.getenv("GOOGLE_API_KEY")
FLASH_MODEL = "gemini-2.0-flash"

# Configure the API
genai.configure(api_key=API_KEY)


def generate_coin_vision(description: str) -> str:
    """
    Generate a comprehensive vision for a cryptocurrency based on name and description.

    Args:
        coin_name: The name of the cryptocurrency
        description: A basic description of the cryptocurrency

    Returns:
        A comprehensive description including vision statement and details
    """
    # Initialize the model
    model = genai.GenerativeModel(
        model_name=FLASH_MODEL,
        generation_config={"temperature": 0.7},
    )

    # Create the prompt for the vision
    prompt = f"""
    Create a comprehensive description for a coin.
    
    Details about the coin:
    {description}
    
    Expand this into a complete description that includes the coin's long-term aspirations, its mission and implementation strategy and target audience.
    
    Format the response as a cohesive paragraph that flows naturally. with 60 words.
    The description should be professional and match the characteristics
    of the coin as described.
    """

    try:
        # Generate the vision using Gemini
        response = model.generate_content(prompt)

        # Extract the text content
        enhanced_description = response.text.strip()

        # Combine with original description
        full_description = f"{description}\n\n{enhanced_description}"

        return full_description

    except Exception as e:
        print(f"Error generating coin vision: {e}")

        # Return a default description if generation fails
        default_vision = ""

        return default_vision
