import os
import openai
from flask import Flask, jsonify, request, session, Response
import requests
from flask_cors import CORS

WEATHER_KEY = os.environ['WEATHER_KEY']
openai.api_key = os.environ['OPENAI_SECRET_KEY']

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
CORS(app, resources={r"*": {"origins": "https://isitglizzyweather.site"}})

@app.route('/', methods=['GET'])
def api_proxy():
    locationQuery = request.args.get('locationQuery')
    response = requests.get(
        f"http://api.weatherapi.com/v1/current.json?q={locationQuery}",
        params={"key": WEATHER_KEY}
    )
    return jsonify(response.json())

@app.route('/chat', methods=["POST"])
def chatbot():
    user_input = request.json.get('prompt')
    if 'messages' not in session:
        session['messages'] = [
            {
                "role": "system",
                "content": (
                    "You are a chatbot. Your personality is positive and helpful. "
                    "Your responses should all relate to hotdogs (also known as, plural 'Glizzies' or singular 'Glizzy') "
                    "in some way. Don't use the word glizzy too often."
                )
            }
        ]
    session["messages"].append({"role": "user", "content": user_input})

    def generate():
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=session["messages"],
            max_tokens=300,
            stream=True
        )
        response_text = ''
        for chunk in response:
            chunk_message = chunk['choices'][0]['delta'].get('content', '')
            response_text += chunk_message
            yield f"data:{chunk_message}\n\n"

        session["messages"].append({"role": "assistant", "content": response_text})

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)