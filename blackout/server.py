# filepath: /home/carles/Escritorio/develop/competicions/hackatonupc/2025/revolut-back/blackout/server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini import main

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

if __name__ == '__main__':
    app.run(debug=True)