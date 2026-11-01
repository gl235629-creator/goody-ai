
import os
from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Goody AI</title>
    <style>
        body { font-family: Arial; background: #f1f5f9;
               margin: 0; padding: 20px; }
        main { max-width: 600px; margin: auto; }
        h1 { color: #2563eb; }
        #chat { background: white; padding: 15px;
                border-radius: 12px; min-height: 250px;
                margin-bottom: 12px; white-space: pre-wrap; }
        input { width: 70%; padding: 12px;
                box-sizing: border-box; }
        button { padding: 12px; background: #2563eb;
                 color: white; border: 0; cursor: pointer; }
        p { overflow-wrap: anywhere; }
    </style>
</head>
<body>
<main>
    <h1>Goody AI</h1>
    <p>Your personal AI assistant</p>
    <div id="chat">Welcome to Goody AI! Ask me anything.</div>
    <form id="form">
        <input id="message" placeholder="Type your question..."
               required>
        <button id="send">Send</button>
    </form>
</main>
<script>
const form = document.getElementById("form");
const chat = document.getElementById("chat");
const input = document.getElementById("message");
const send = document.getElementById("send");

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const message = input.value.trim();
    if (!message) return;

    chat.textContent += "\\n\\nYou: " + message + "\\nGoody AI: Thinking...";
    input.value = "";
    send.disabled = true;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message})
        });
        const data = await response.json();
        chat.textContent = chat.textContent.replace(
            "Thinking...", data.reply || data.error || "No response."
        );
    } catch (error) {
        chat.textContent += "\\nSorry, something went wrong.";
    } finally {
        send.disabled = false;
    }
});
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    message = (request.json or {}).get("message", "").strip()
    if not message:
        return jsonify(error="Please type a question."), 400

    if not os.environ.get("OPENAI_API_KEY"):
        return jsonify(error="API key is missing in Render."), 500

    try:
        client = OpenAI()
        response = client.responses.create(
            model="gpt-5.5",
            instructions="You are Goody AI, a friendly and helpful assistant.",
            input=message
        )
        return jsonify(reply=response.output_text)
    except Exception:
        app.logger.exception("AI request failed")
        return jsonify(
            error="AI request failed. Check your API key, API credits, and logs."
        ), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
