from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import requests

app = Flask(__name__)
CORS(app)

# Replace with your actual key securely in production
RAPIDAPI_KEY = "7091642a6fmsh386fe0f50773707p18d80cjsn770fc45bef8b"
RAPIDAPI_HOST = "translate-plus.p.rapidapi.com"

MEMORY_FILE = "chat_memory.json"

if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as file:
        memory = json.load(file)
else:
    memory = {}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").lower()

    if user_input in memory:
        response = memory[user_input]
    else:
        # Try using RapidAPI language translation
        try:
            url = "https://translate-plus.p.rapidapi.com/translate"
            payload = {
                "text": user_input,
                "source": "auto",
                "target": "en"
            }
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": RAPIDAPI_KEY,
                "X-RapidAPI-Host": RAPIDAPI_HOST
            }

            api_response = requests.post(url, json=payload, headers=headers)
            result = api_response.json()
            response = result.get("translated_text", {}).get("en", "I couldn't translate that.")
        except Exception as e:
            response = "I couldn't understand or translate that."

    return jsonify({"response": response})

@app.route("/teach", methods=["POST"])
def teach():
    data = request.get_json()
    question = data.get("question", "").lower()
    answer = data.get("answer", "")
    memory[question] = answer
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file)
    return jsonify({"status": "learned", "question": question})

if __name__ == "__main__":
    app.run(port=5000)
