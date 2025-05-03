import google.generativeai as genai
from typing import List, Any, TypedDict
import random
from .game_data import TARGETS, AREAS, EVENT_TYPES
from ..models import Situation
API_KEY = "AIzaSyDZyBoLtY9TKlrDQlEYWYf6H4mZKSv2Uj8"
FLASH_MODEL = "gemini-2.0-flash"
PRO_MODEL = "gemini-2.0-pro"
MAX_HISTORY = 15

genai.configure(api_key=API_KEY)


class Choice(TypedDict):
    text: str
    consequence: str
    updated_value: Any  # You can be more specific if you know the type


class SituationOutput(TypedDict):
    situation: str
    category: str
    choices: List[Choice]


class SituationGenerator:
    def __init__(self, coin_id=None):
        self.api_key = API_KEY
        self.model_name = FLASH_MODEL
        self.model = None
        self.coin_id = coin_id
        self._configure()

    def _configure(self):
        genai.configure(api_key=self.api_key)

        # Define the function declaration using the newer approach
        situation_function = {
            "name": "print_situation",
            "description": "Outputs a scenario for a cryptocurrency game",
            "parameters": {
                "type": "object",
                "properties": {
                    "situation": {
                        "type": "string",
                        "description": "The scenario presented to the player",
                    },
                    "category": {
                        "type": "string",
                        "description": "The category of the scenario",
                    },
                    "choices": {
                        "type": "array",
                        "description": "The choices available to the player",
                        "items": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string"},
                                "consequence": {"type": "string"},
                                "updated_value": {"type": "number"},
                            },
                        },
                    },
                },
                "required": ["situation", "category", "choices"],
            },
        }

        # Create tools list with function declarations
        tools = [{"function_declarations": [situation_function]}]

        # Configure the model with tools
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={"temperature": 0.7},
            tools=tools,
        )

    def get_previous_situations(self):
        """Get previous situations for the coin from the database."""
        # Only attempt to get history if we have a coin_id
        if not self.coin_id:
            return []
        
        # Get the last 15 situations for this coin, ordered by created_at descending
        previous_situations = Situation.objects.filter(
            coin_id=self.coin_id
        ).order_by('-created_at')[:MAX_HISTORY]
        
        # Convert to a format similar to what we used before
        return [
            {
                "situation": situation.description,
                "category": situation.category,
                "selected_choice": situation.selected_choice or situation.choices[0]["id"],
                "choices": situation.choices,
            }
            for situation in previous_situations
        ]

    @staticmethod
    def parse_response(response) -> dict:
        # Extract function call from the response
        function_call = response.candidates[0].content.parts[0].function_call
        return {
            "situation": function_call.args["situation"],
            "category": function_call.args["category"],
            "choices": [
                {**choice, "id": chr(65 + i)}
                for i, choice in enumerate(function_call.args["choices"])
            ],
        }

    def send_to_model(self, prompt: str) -> dict:
        response = self.model.generate_content(prompt)
        parsed_response = self.parse_response(response)
        return parsed_response

    def get_continuity_prompt(self, coin_name: str, coin_value: float) -> str:
        """Get a prompt for the Gemini model with continuity from database."""
        # Pick random items from our predefined lists for variety
        target = random.choice(TARGETS)
        area = random.choice(AREAS)
        event_type = random.choice(EVENT_TYPES)
        
        # Get previous situations from the database
        previous_situations = self.get_previous_situations()
        
        # Base prompt if no history
        if not previous_situations:
            return f"""
            Create a scenario for an interactive role-playing game similar to 
            REIGNS, where the player manages a cryptocurrency called {coin_name} 
            currently valued at ${coin_value:.2f}.

            The scenario should involve a {target} in a {area} dealing with a 
            {event_type}. Present exactly 2 choices to the player.
            For each choice, provide a consequence and updated coin value.

            Keep the tone similar to REIGNS - sometimes serious, sometimes 
            absurd or unexpected.
            """
        
        # Build continuity prompt with history from database
        history_items = []
        for item in previous_situations:  # Use last 5 for context
            choice_text = "unknown"
            if item.get("selected_choice"):
                choices = item.get("choices", [])
                for choice in choices:
                    if choice.get("id") == item["selected_choice"]:
                        choice_text = choice.get("text", "unknown")
                        break
            
            history_items.append(
                f"- {item['situation']} (Player chose: {choice_text})"
            )
            
        history_summary = "\n".join(history_items)
        
        return f"""
        Create the next scenario for an interactive role-playing cryptocurrency 
        game where the player manages a coin called {coin_name} currently 
        valued at ${coin_value:.2f}.
        
        Previous story elements:
        {history_summary}
        
        The new scenario should maintain continuity with these previous events 
        while introducing a {target} in a {area} dealing with a {event_type}.
        
        IMPORTANT: Do not repeat previous scenarios. Create a fresh situation 
        that builds on the story. Present exactly 2 choices to the player.
        
        For each choice, provide a consequence and updated coin value.
        Keep the tone similar to REIGNS - sometimes serious, sometimes absurd 
        or unexpected.
        """


def get_game_situation(coin_name: str, coin_value: float, coin_id=None):
    """Get a standardized game situation for the frontend with continuity."""
    generator = SituationGenerator(coin_id=coin_id)
    
    # Generate a new situation using continuity from database
    prompt = generator.get_continuity_prompt(coin_name, coin_value)
    result = generator.send_to_model(prompt)
    
    # The situation ID will be created by the database
    return result
