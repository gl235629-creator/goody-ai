from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Goody AI</title>
        <style>
            body {
                background: #101827;
                color: white;
                font-family: Arial;
                text-align: center;
                padding: 40px;
            }
            input {
                padding: 15px;
                width: 70%;
                border-radius: 10px;
            }
            button {
                padding: 15px;
                background: #00bfa5;
                border: none;
                border-radius: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to Goody AI</h1>
        <p>Your personal AI assistant</p>
        <form action="/chat" method="post">
            <input name="message" placeholder="Ask Goody AI anything..." required>
            <button type="submit">Send</button>
        </form>
    </body>
    </html>
    """

@app.route("/chat", methods=["POST"])
def chat():
    message = request.form.get("message", "")

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=message
        )
        return "<h2>Goody AI</h2><p>" + response.output_text + "</p><a href='/'>Ask again</a>"
    except Exception as e:
        return "Error: " + str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
