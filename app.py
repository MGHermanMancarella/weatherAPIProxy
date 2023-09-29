import os
import openai
from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

WEATHER_KEY = os.environ['WEATHER_KEY']
openai.api_key = os.environ['OPENAI_SECRET_KEY']

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "https://isitglizzyweather.site"}})

@app.route('/', methods=['GET'])
def api_proxy():
    # Retrieve the locationQuery query parameter
    locationQuery = request.args.get('locationQuery')

    # print(locationQuery)
    # print(WEATHER_KEY)

    # Use the requests library to call the external API
    response = requests.get(f"http://api.weatherapi.com/v1/current.json?q={locationQuery}",
                            params={"key": WEATHER_KEY})

    # Return the response to our static site
    return jsonify(response.json())

@app.route('/chat', methods=["POST"])
def chatbot():
    prompt = request.args.get('prompt')
    messages= [{"role": "system", "content": f"You are a chatbot. Your personality is drunk and in love. Your responses should all relate to hotdogs (also known as, pleural 'Glizzies' or singular 'Glizzy') in some way."}]

    user_input = prompt("User: ")
    messages.append({"role": "user", "content": user_input})
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    messages.append(res['choices'][0]['message'].to_dict())
    return ("Glizzy_Bot: ", res['choices'][0]['message']['content'])
