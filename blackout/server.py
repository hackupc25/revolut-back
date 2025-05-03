from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini import main
import os
import pandas as pd

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return "Welcome to the Blackout API! Use the /generate endpoint to get recommendations."

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    user_id = data.get('user_id')
    duration_days = data.get('duration_days', 3)
    try:
        result = main(user_id, duration_days)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/transactions', methods=['GET'])
def get_transactions():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"success": False, "error": "User ID is required"}), 400

    # Path to the datasets/users folder
    base_path = os.path.join(os.getcwd(), 'datasets', 'users')
    file_path = os.path.join(base_path, f'user{user_id}.csv')

    # Check if the file exists
    if not os.path.exists(file_path):
        return jsonify({"success": False, "error": f"No data found for user {user_id}"}), 404

    # Read the CSV file
    try:
        df = pd.read_csv(file_path)
        transactions = df.to_dict(orient='records')  # Convert to a list of dictionaries
        return jsonify({"success": True, "transactions": transactions})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)