import os
from flask import Flask, jsonify, request
import requests

WEATHER_KEY = os.environ['WEATHER_KEY']

app = Flask(__name__)

@app.route('/weatherapi/proxy', methods=['GET'])
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
