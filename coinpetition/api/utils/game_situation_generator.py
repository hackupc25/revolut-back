import google.generativeai as genai
from typing import Dict, List, Any
import random
import json


API_KEY = "AIzaSyDZyBoLtY9TKlrDQlEYWYf6H4mZKSv2Uj8"
FLASH_MODEL = "gemini-1.5-flash"
PRO_MODEL = "gemini-1.5-pro"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(model_name=FLASH_MODEL)


class GameState:
    def __init__(self, coin_name: str, initial_value: float):
        self.coin_name = coin_name
        self.coin_value = initial_value
        self.history: List[Dict] = []
        self.event_categories = []

    def add_event(
        self,
        situation: str,
        category: str,
        choice: str,
        consequence: str,
        value_change: float,
    ):
        self.coin_value += value_change

        self.history.append(
            {
                "situation": situation,
                "category": category,
                "choice": choice,
                "consequence": consequence,
                "value_after": self.coin_value,
            }
        )

        # Track the category to ensure variety
        self.event_categories.append(category)

    def get_history_summary(self) -> str:
        if not self.history:
            return (f"New cryptocurrency {self.coin_name} valued at "
                    f"${self.coin_value}.")

        summary = (f"History of {self.coin_name} "
                   f"(currently ${self.coin_value:.2f}):\n")
        
        for i, event in enumerate(self.history[-3:], 1):
            idx = len(self.history) - 3 + i
            summary += f"Event {idx}: {event['situation']} "
            summary += f"Choice: {event['choice']}. "
            summary += f"Result: {event['consequence']} "
            summary += f"Value: ${event['value_after']:.2f}\n"

        return summary

    def get_suggested_categories(self) -> List[str]:
        """Return categories that haven't been used recently."""
        all_categories = [
            "economic",
            "political",
            "technological",
            "social",
            "environmental",
            "security",
            "regulatory",
            "competition",
            "partnership",
            "innovation",
            "scandal",
            "natural_disaster",
            "celebrity",
            "global_market",
        ]

        # Avoid repeating the last 3 categories if possible
        recent = self.event_categories[-3:] if self.event_categories else []
        suggested = [c for c in all_categories if c not in recent]

        # If we've exhausted all categories, just use any
        if not suggested:
            suggested = all_categories

        return random.sample(suggested, min(3, len(suggested)))


# Define function schema for Gemini model
SCHEMA = {
    "name": "generate_crypto_scenario",
    "description": "Generate a cryptocurrency game scenario with choices",
    "parameters": {
        "type": "object",
        "properties": {
            "situation": {
                "type": "string",
                "description": "A scenario that affects the cryptocurrency"
            },
            "category": {
                "type": "string",
                "description": "Category of the scenario",
                "enum": [
                    "economic", "political", "technological", "social", 
                    "environmental", "security", "regulatory", "competition",
                    "partnership", "innovation", "scandal", "natural_disaster", 
                    "celebrity", "global_market"
                ]
            },
            "choices": {
                "type": "array",
                "description": "Exactly 2 choices with their consequences",
                "items": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Description of the choice"
                        },
                        "consequence": {
                            "type": "string",
                            "description": "Result of making this choice"
                        },
                        "new_value": {
                            "type": "number",
                            "description": "New value after this choice"
                        }
                    },
                    "required": ["text", "consequence", "new_value"]
                },
                "minItems": 2,
                "maxItems": 2
            }
        },
        "required": ["situation", "category", "choices"]
    }
}


def generate_situation(game_state: GameState) -> Dict[str, Any]:
    """Generate a new game situation using function calling with Gemini."""
    history_summary = game_state.get_history_summary()
    suggested_categories = game_state.get_suggested_categories()

    prompt = f"""
    Create a scenario for an interactive role-playing game similar to REIGNS, 
    where the player manages a cryptocurrency called {game_state.coin_name} 
    currently valued at ${game_state.coin_value:.2f}.

    Previous history and current state:
    {history_summary}

    Create a new scenario from one of these suggested categories: 
    {', '.join(suggested_categories)}

    The scenario should present a situation and exactly 2 choices.
    For each choice, provide a consequence and updated coin value.

    Keep the tone similar to REIGNS - sometimes serious, sometimes absurd or 
    unexpected. Include diverse characters and situations.
    """

    # Make the function call
    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0.8},
        tools=[SCHEMA]
    )
    
    # Extract and return the function response
    function_response = response.candidates[0].content.parts[0].function_call
    result = json.loads(function_response.args)
    
    return result


def standardize_response(scenario: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Convert the scenario to a standardized response format."""
    choices = []
    
    for choice in scenario["choices"]:
        choices.append({
            "situation": scenario["situation"],
            "category": scenario["category"],
            "choice_text": choice["text"],
            "consequence": choice["consequence"],
            "updated_value": choice["new_value"]
        })
    
    return choices


def apply_choice(
    game_state: GameState,
    choice_data: Dict[str, Any],
    choice_index: int
) -> None:
    """Apply the selected choice to the game state."""
    value_change = choice_data["updated_value"] - game_state.coin_value
    choice_letter = "A" if choice_index == 0 else "B"

    game_state.add_event(
        situation=choice_data["situation"],
        category=choice_data["category"],
        choice=f"{choice_letter}: {choice_data['choice_text']}",
        consequence=choice_data["consequence"],
        value_change=value_change,
    )


def get_game_situation(coin_name: str, coin_value: float, history: List[Dict] = None) -> List[Dict[str, Any]]:
    """Get a standardized game situation for the frontend."""
    if history is None:
        history = []
        
    # Create a temporary game state to generate a situation
    game_state = GameState(coin_name, coin_value)
    game_state.history = history
    
    # Record categories from history
    for event in history:
        game_state.event_categories.append(event["category"])
    
    # Generate the raw scenario
    raw_scenario = generate_situation(game_state)
    
    # Standardize the response
    return standardize_response(raw_scenario)


if __name__ == "__main__":
    print("Interactive Cryptocurrency Simulator\n")

    # Initialize the game state
    coin_name = "CryptoCoin"
    initial_value = 1000.0
    game_state = GameState(coin_name, initial_value)

    # Simulate rounds
    rounds = 5
    for round_num in range(1, rounds + 1):
        print(f"\nROUND {round_num}/{rounds}")

        # Generate choices
        choices = get_game_situation(game_state.coin_name, game_state.coin_value, game_state.history)
        
        # Display situation and choices
        print(f"\n{choices[0]['situation']}")
        print(f"Category: {choices[0]['category']}")
        print("\nYour choices:")
        print(f"A: {choices[0]['choice_text']}")
        print(f"B: {choices[1]['choice_text']}")

        # Get user choice
        while True:
            choice_letter = input("Select choice (A/B): ").strip().upper()
            if choice_letter in ["A", "B"]:
                break
            print("Invalid choice. Please enter A or B.")

        # Apply the selected choice
        choice_index = 0 if choice_letter == "A" else 1
        apply_choice(game_state, choices[choice_index], choice_index)

        # Show the outcome
        print(f"\nOutcome: {choices[choice_index]['consequence']}")
        print(f"New value: ${choices[choice_index]['updated_value']:.2f}")
        print(f"\n{'='*50}")
        print(f" {game_state.coin_name} VALUE: ${game_state.coin_value:.2f}")
        print(f"{'='*50}")

    # Print final history
    print("\nFULL HISTORY:")
    for i, event in enumerate(game_state.history, 1):
        print(f"Event {i}: [{event['category']}] {event['situation']}")
        print(f"Choice: {event['choice']}")
        print(f"Result: {event['consequence']}")
        print(f"Value: ${event['value_after']:.2f}")
        print()
