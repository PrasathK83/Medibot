import os
from flask import Flask, request, jsonify, send_from_directory
import requests
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("Please set the GROQ_API_KEY in your .env file")

app = Flask(__name__)
CORS(app)  

@app.route("/")
def home():
    return send_from_directory(os.path.dirname(__file__), "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
    "model": "llama3-8b-8192",
    "messages": [
        {"role": "system", "content": (
            "You are a helpful medical assistant bot. "
            "Only answer questions related to health, medicine, and medical topics. "
            "For any questions outside this scope, reply: "
            "\"As I am a medical bot I don't know about that.Ask me About the Questions that related to Your Health or Medical topics.\""
        )},
        {"role": "user", "content": user_message}
    ]
}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        return jsonify({"reply": f"Error: {response.text}"}), 500

    result = response.json()
    bot_reply = result["choices"][0]["message"]["content"]

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port, debug=True)

