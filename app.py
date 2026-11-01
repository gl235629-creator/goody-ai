
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Goody AI</title>
    </head>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1>Welcome to Goody AI!</h1>
        <p>Your AI application is running.</p>
    </body>
    </html>
    """

@app.route("/health")
def health():
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
