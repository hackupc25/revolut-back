import google.generativeai as genai
import pandas as pd

API_KEY = "AIzaSyDZyBoLtY9TKlrDQlEYWYf6H4mZKSv2Uj8"
FLASH_MODEL = "gemini-1.5-flash"
PRO_MODEL = "gemini-1.5-pro"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(model_name=FLASH_MODEL)

def generate_cash_plan(transactions, duration_days=3):
    prompt = f"""
    Assume there will be a power outage lasting {duration_days} days, with no electricity or internet access.
    A user wants to know how much cash they should carry to be prepared, based on their recent spending history.

    User's recent transactions (format: date - category - amount):
    {transactions}

    Your task:
    1. Estimate the amount of cash (in euros) they should carry
    2. Briefly explain how you calculated it
    3. Highlight the most important spending categories during such a scenario

    Be concise, realistic, and helpful.
    """
    response = model.generate_content(prompt)
    return response.text

def load_user_csv(user_id):
    filename = f"./datasets/users/user{user_id}.csv"
    df = pd.read_csv(filename)
    transaction_str = "\n".join(
        f"{row['date']} - {row['category']} - €{row['amount']}"
        for _, row in df.iterrows()
    )
    return transaction_str

def main(user_id, duration_days=3):
    transactions = load_user_csv(user_id)
    result = generate_cash_plan(transactions, duration_days)
    return result
