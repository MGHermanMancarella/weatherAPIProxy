import os
from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

WEATHER_KEY = os.environ['WEATHER_KEY']

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://isitglizzyweather.site/HereBeGlizzies.html"}})

@app.route('/', methods=['GET'])
def api_proxy():
    # Retrieve the locationQuery query parameter
    locationQuery = request.args.get('locationQuery')

    print(locationQuery)
    print(WEATHER_KEY)

    # Use the requests library to call the external API
    response = requests.get(f"http://api.weatherapi.com/v1/current.json?q={locationQuery}",
                            params={"key": WEATHER_KEY})

    # Return the response to our static site
    return jsonify(response.json())
