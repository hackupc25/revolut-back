import google.generativeai as genai
from typing import List, Any, TypedDict

API_KEY = "AIzaSyDZyBoLtY9TKlrDQlEYWYf6H4mZKSv2Uj8"
FLASH_MODEL = "gemini-2.0-flash"
PRO_MODEL = "gemini-2.0-pro"

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
    def __init__(self):
        self.api_key = API_KEY
        self.model_name = FLASH_MODEL
        self.model = None
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
                        "description": "The scenario presented to the player"
                    },
                    "category": {
                        "type": "string",
                        "description": "The category of the scenario"
                    },
                    "choices": {
                        "type": "array", 
                        "description": "The choices available to the player",
                        "items": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string"},
                                "consequence": {"type": "string"},
                                "updated_value": {"type": "number"}
                            }
                        }
                    }
                },
                "required": ["situation", "category", "choices"]
            }
        }
        
        # Create tools list with function declarations
        tools = [{"function_declarations": [situation_function]}]
        
        # Configure the model with tools
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={"temperature": 0.7},
            tools=tools
        )
    
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
            ]
        }

    def send_to_model(self, prompt: str) -> dict:
        response = self.model.generate_content(prompt)
        return self.parse_response(response)

    @staticmethod
    def get_prompt(coin_name: str, coin_value: float) -> str:
        """Get a prompt for the Gemini model."""
        return f"""
        Create a scenario for an interactive role-playing game similar to 
        REIGNS, where the player manages a cryptocurrency called {coin_name} 
        currently valued at ${coin_value:.2f}.

        The scenario should present a situation and exactly 2 choices.
        For each choice, provide a consequence and updated coin value.

        Keep the tone similar to REIGNS - sometimes serious, sometimes absurd 
        or unexpected. Include diverse characters and situations.
        """


def get_game_situation(coin_name: str, coin_value: float):
    """Get a standardized game situation for the frontend."""
    prompt = SituationGenerator.get_prompt(coin_name, coin_value)
    return SituationGenerator().send_to_model(prompt)
