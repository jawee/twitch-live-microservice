from flask import Flask, request, jsonify
import requests, json
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

client_secret = os.getenv("CLIENT_SECRET")
client_id = os.getenv("CLIENT_ID")

def get_token():
    url = 'https://id.twitch.tv/oauth2/token?client_id=' + client_id + '&client_secret='+client_secret+'&grant_type=client_credentials'
    r = requests.post(url)
    access_token = r.json()['access_token']

    return r.json()['access_token']

@app.route('/', methods=['POST'])
def get_tasks():
    args = request.json

    query_parameters = '';
    for i in request.json['channels']:
        query_parameters += 'user_login=' + i + '&'
    token = get_token()
    url = 'https://api.twitch.tv/helix/streams?'

    full_url = url + query_parameters

    full_url = full_url[:-1]

    headers = {'Client-ID': client_id, 'Authorization': 'Bearer ' + token}
    r = requests.get(full_url, headers=headers)

    return r.json()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 5000,debug=True)