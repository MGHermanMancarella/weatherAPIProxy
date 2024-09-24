import os
import openai
from flask import Flask, jsonify, request, session
import requests
from flask_cors import CORS

WEATHER_KEY = os.environ['WEATHER_KEY']
openai.api_key = os.environ['OPENAI_SECRET_KEY']

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
CORS(app, resources={r"*": {"origins": "https://isitglizzyweather.site"}})
# CORS(app, resources={r"/*": {"origins": "*"}})


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

    user_input = request.json.get('prompt')
    if 'messages' not in session:
        session['messages'] = [
            {"role": "system",
            "content": f"You are a chatbot. Your personality is positive and helpful. Your responses should all relate to hotdogs (also known as, pleural 'Glizzies' or singular 'Glizzy') in some way. Don't use the word glizzy too often."
            }
        ]
    session["messages"].append({"role": "user", "content": user_input})

    res = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=session["messages"],
        max_tokens=300
    )
    response_message = res['choices'][0]['message'].to_dict()
    session["messages"].append(
        {"role": "assistant", "content": response_message['content']})
    print(response_message)
    return jsonify({"Glizzy_Bot": response_message['content']})
