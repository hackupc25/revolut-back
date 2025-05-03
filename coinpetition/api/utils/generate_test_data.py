"""
Django management command to generate test data.
"""
import random
from datetime import datetime, timedelta
from api.models import GameSession, GameCoin, CoinValueHistory

def generate_test_data(coin: GameCoin):
    # Generate historical data for the past 30 days
    end_date = datetime.now()
    
    value = round(random.uniform(80.0, 120.0), 2)
    
    for day in range(30):
        # Calculate the date for this data point
        date = end_date - timedelta(days=day)
        
        # For historical data, vary the value by a random percentage
        # More recent days should be closer to the current value
        volatility = 0.2 * (day / 30)  # Increasing volatility over time
        change_percentage = random.uniform(-volatility, volatility)
        value = value / (1 + change_percentage)  # Working backwards
        
        # Ensure the value is within a reasonable range
        value = max(min(value, 200.0), 50.0)
        rounded_value = round(value, 2)
        
        # Create historical record
        CoinValueHistory.objects.create(
            coin=coin,
            timestamp=date,
            value=rounded_value
        )