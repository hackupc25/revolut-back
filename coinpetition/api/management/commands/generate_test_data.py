"""
Django management command to generate test data.
"""
import random
import uuid
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from api.models import GameSession, GameCoin, CoinValueHistory


class Command(BaseCommand):
    help = 'Generates a game session with 4 coins and 30 days of historical data'

    def handle(self, *args, **options):
        # Create a new game session
        session_id = str(uuid.uuid4())
        session = GameSession.objects.create(session_id=session_id)
        self.stdout.write(self.style.SUCCESS(f'Created game session with ID: {session_id}'))

        # Create 4 coins
        coin_names = ['BitCoin', 'Ethereum', 'CoinX', 'MoonCoin']
        coins = []
        
        for name in coin_names:
            # Generate a random starting value between 80 and 120
            current_value = round(random.uniform(80.0, 120.0), 2)
            coin = GameCoin.objects.create(
                game_session=session,
                coin_name=name,
                current_value=current_value
            )
            coins.append(coin)
            self.stdout.write(self.style.SUCCESS(f'Created coin: {name} with value: {current_value}'))

        # Generate historical data for the past 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        for coin in coins:
            # Start with the current value and work backwards
            value = coin.current_value
            
            for day in range(30):
                # Calculate the date for this data point
                date = end_date - timedelta(days=day)
                
                # For historical data, vary the value by a random percentage between -3% and +3%
                # More recent days should be closer to the current value
                volatility = 0.2 * (day / 30)  # Increasing volatility as we go further back in time
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
            
            # Count the history records created for this coin
            history_count = CoinValueHistory.objects.filter(coin=coin).count()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created {history_count} historical records for {coin.coin_name}'
                )
            )

        total_coins = GameCoin.objects.filter(game_session=session).count()
        total_history = CoinValueHistory.objects.filter(coin__game_session=session).count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created 1 session, {total_coins} coins, and {total_history} historical data points'
            )
        ) 