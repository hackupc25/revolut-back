import google.generativeai as genai
from typing import List
from ..models import Situation

API_KEY = "AIzaSyDZyBoLtY9TKlrDQlEYWYf6H4mZKSv2Uj8"
FLASH_MODEL = "gemini-2.0-flash"


class SituationSummaryGenerator:
    def __init__(self):
        self.api_key = API_KEY
        self.model_name = FLASH_MODEL
        self.model = None
        self._configure()

    def _configure(self):
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={"temperature": 0.2, "max_output_tokens": 100}
        )

    def get_past_situations(self, coin_id: int, max_situations: int = 5) -> List[dict]:
        """Get past situations for the specified coin."""
        past_situations = Situation.objects.filter(
            coin_id=coin_id
        ).order_by("-created_at")[:max_situations]
        
        # Format situations in a way that's easy to summarize
        formatted_situations = []
        for situation in past_situations:
            choice_text = "unknown"
            if situation.selected_choice:
                for choice in situation.choices:
                    if choice.get("id") == situation.selected_choice:
                        choice_text = choice.get("text", "unknown")
                        break
            
            formatted_situations.append({
                "situation": situation.description,
                "choice": choice_text
            })
            
        return formatted_situations

    def generate_summary(self, coin_name: str, past_situations: List[dict]) -> str:
        """Generate a summary of past situations using Gemini."""
        if not past_situations:
            return "No past situations available for this coin."
            
        # Create a formatted string of past situations
        situations_text = ""
        for i, situation in enumerate(past_situations):
            situations_text += f"Situation {i+1}: {situation['situation']}\n"
            situations_text += f"Player chose: {situation['choice']}\n\n"
            
        # Create the prompt for Gemini
        prompt = f"""
        Below are the last {len(past_situations)} situations that happened to the 
        cryptocurrency {coin_name}:
        
        {situations_text}
        
        Provide a concise summary (maximum 60 words) that captures the key events 
        and decisions made for {coin_name}. Focus on the narrative thread 
        connecting these situations.
        """
        
        try:
            response = self.model.generate_content(prompt)
            print(response.text.strip())
            return response.text.strip()
        except Exception as e:
            print(f"Error generating summary: {e}")
            return f"Error generating summary for {coin_name}"


def get_situation_summary(
    coin_name: str, coin_id: int, max_situations: int = 5
) -> str:
    """Get a summary of past situations for the given coin."""
    generator = SituationSummaryGenerator()
    past_situations = generator.get_past_situations(coin_id, max_situations)
    return generator.generate_summary(coin_name, past_situations) 