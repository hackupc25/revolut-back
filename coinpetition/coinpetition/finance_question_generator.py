import requests
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
API_ENDPOINT_BASE = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash"

def generate_question() -> str:
    """Calls the Google Gemini API to generate content."""
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY not configured. Please set the environment variable."

    api_url = f"{API_ENDPOINT_BASE}:generateContent?key={GEMINI_API_KEY}"

    prompt = """
            You are a financial education expert designing a multiple-choice question for a daily quiz game where friends compete to test their financial knowledge.

            Your task is to generate one question per prompt, focused on everyday personal finance and investing — such as index funds, budgeting, savings strategies, credit scores, inflation, interest rates, and financial planning.

            Return your response as a JSON object with the following structure:

            {
                "question": "Your question here",
                "options": {
                    "A": "Option A text",
                    "B": "Option B text",
                    "C": "Option C text",
                    "D": "Option D text"
                },
                "correct_answer": "Letter of correct answer (A/B/C/D)",
                "explanation": "Brief explanation (1-2 sentences) explaining why the correct answer is right."
            }

            Guidelines:
                - The question must be short and clear (1-2 sentences).
                - One answer should be clearly incorrect (a red herring), and the others should be plausible but incorrect.
                - The correct answer should not be too obvious, and should require some thought.
                - Focus only on concepts relevant to the average person (e.g., index funds, emergency savings, interest, credit, budgeting).
                - Use a casual, engaging tone, but keep information accurate and useful.
                - Target a general audience aged 16 and up with basic-to-intermediate financial knowledge.
    """

    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Process the response based on the Gemini API structure
        result = response.json()
        # Expected structure: {"candidates": [{"content": {"parts": [{"text": "..."}]}}]}
        if (
            result
            and "candidates" in result
            and result["candidates"]
            and "content" in result["candidates"][0]
            and "parts" in result["candidates"][0]["content"]
            and result["candidates"][0]["content"]["parts"]
        ):
            return result["candidates"][0]["content"]["parts"][0].get("text", "Error: Could not parse Gemini response text")
        # Handle potential safety blocks or other response variations
        elif "promptFeedback" in result and "blockReason" in result["promptFeedback"]:
             return f"Error: Request blocked due to {result['promptFeedback']['blockReason']}"
        else:
            # Log the unexpected format for debugging
            print(f"Unexpected Gemini response format: {result}")
            return "Error: Unexpected Gemini response format"

    except requests.exceptions.RequestException as e:
        # Log the full error for debugging
        print(f"Error calling Gemini API: {e}")
        if e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        return f"Error: {e}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"Error: {e}"

if __name__ == '__main__':
    response_text = generate_question()
    print(f"Gemini Response:\n{response_text}") 
