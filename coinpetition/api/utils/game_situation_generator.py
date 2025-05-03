"""
Game situation generator for Coinpetition.
This module provides functions to generate game situations and handle player choices.
"""

class GameState:
    """Class to represent the current state of a game."""
    
    def __init__(self, coin_name, coin_value):
        self.coin_name = coin_name
        self.coin_value = coin_value
        self.metrics = {
            'popularity': 50,
            'tech_innovation': 50,
            'regulation_risk': 50,
            'investor_confidence': 50,
            'global_adoption': 30,
        }
        self.event_categories = []

def generate_situation(game_state):
    """Generate a new game situation based on current game state."""
    # Simple implementation - in a real app this might use GPT or other logic
    return """
    SITUATION: There's a rumor that a major retailer is considering accepting your coin.
    CATEGORY: adoption
    CHOICE_A: Confirm the rumor publicly
    CONSEQUENCE_A: The retailer denies the rumor, causing a temporary drop in confidence
    NEW_VALUE_A: 95
    METRICS_A: {"popularity": 55, "tech_innovation": 50, "regulation_risk": 50, "investor_confidence": 45, "global_adoption": 35}
    CHOICE_B: Reach out to the retailer privately to discuss partnership
    CONSEQUENCE_B: The retailer expresses interest and begins discussions
    NEW_VALUE_B: 105
    METRICS_B: {"popularity": 52, "tech_innovation": 50, "regulation_risk": 50, "investor_confidence": 55, "global_adoption": 38}
    """

def parse_situation_response(response_text):
    """Parse the response text into structured data."""
    lines = response_text.strip().split('\n')
    situation = ""
    category = ""
    choice_a = {}
    choice_b = {}
    
    for line in lines:
        line = line.strip()
        if line.startswith('SITUATION:'):
            situation = line.replace('SITUATION:', '').strip()
        elif line.startswith('CATEGORY:'):
            category = line.replace('CATEGORY:', '').strip()
        elif line.startswith('CHOICE_A:'):
            choice_a['text'] = line.replace('CHOICE_A:', '').strip()
        elif line.startswith('CONSEQUENCE_A:'):
            choice_a['consequence'] = line.replace('CONSEQUENCE_A:', '').strip()
        elif line.startswith('NEW_VALUE_A:'):
            choice_a['new_value'] = float(line.replace('NEW_VALUE_A:', '').strip())
        elif line.startswith('METRICS_A:'):
            metrics_str = line.replace('METRICS_A:', '').strip()
            # Simple parsing - in real app use json.loads
            metrics = {}
            for item in metrics_str.strip('{}').split(','):
                k, v = item.split(':')
                metrics[k.strip(' "')] = int(v.strip())
            choice_a['metrics'] = metrics
        elif line.startswith('CHOICE_B:'):
            choice_b['text'] = line.replace('CHOICE_B:', '').strip()
        elif line.startswith('CONSEQUENCE_B:'):
            choice_b['consequence'] = line.replace('CONSEQUENCE_B:', '').strip()
        elif line.startswith('NEW_VALUE_B:'):
            choice_b['new_value'] = float(line.replace('NEW_VALUE_B:', '').strip())
        elif line.startswith('METRICS_B:'):
            metrics_str = line.replace('METRICS_B:', '').strip()
            # Simple parsing - in real app use json.loads
            metrics = {}
            for item in metrics_str.strip('{}').split(','):
                k, v = item.split(':')
                metrics[k.strip(' "')] = int(v.strip())
            choice_b['metrics'] = metrics
    
    return situation, category, choice_a, choice_b

def apply_choice(game_state, situation, category, choice_data, choice_letter):
    """Apply the consequences of a choice to the game state."""
    game_state.coin_value = choice_data.get('new_value', game_state.coin_value)
    if 'metrics' in choice_data:
        game_state.metrics.update(choice_data['metrics'])
    return game_state 