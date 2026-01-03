from flask import Flask, request, Response, session
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "neon_ai_secret"
CORS(app, supports_credentials=True)

client = OpenAI()

SYSTEM_PROMPT = """
You are Neon AI, a friendly and intelligent assistant.
Respond naturally, clearly, and conversationally.
"""

@app.route("/stream", methods=["POST"])
def stream_chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if "history" not in session:
        session["history"] = []

    session["history"].append({"role": "user", "content": user_message})

    def generate():
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT}
            ] + session["history"],
            stream=True
        )

        full_reply = ""

        for chunk in stream:
            if chunk.choices[0].delta.get("content"):
                token = chunk.choices[0].delta["content"]
                full_reply += token
                yield token

        session["history"].append({"role": "assistant", "content": full_reply})

    return Response(generate(), mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True)
