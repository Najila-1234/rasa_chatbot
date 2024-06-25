from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Define Rasa server URL
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json['message']

    # Send user message to Rasa server
    payload = {
        "sender": "user",
        "message": user_message
    }
    headers = {
        'Content-Type': 'application/json'
    }
    rasa_response = requests.post(RASA_SERVER_URL, json=payload, headers=headers)

    # Extract bot response
    if rasa_response.status_code == 200:
        bot_response = rasa_response.json()[0]['text']
    else:
        bot_response = "Sorry, I couldn't understand that."

    return jsonify({'message': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
