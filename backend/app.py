from flask import Flask, render_template, request
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restx import Resource, Api

#API Using: https://dashboard.api-football.com/
#API Directions/Flowchart: https://www.api-football.com/documentation-v3#section/Authentication/API-SPORTS-Account



import json

app = Flask(__name__)

api= Api(app, title='Stat11', description="API for Statll app")
cors = CORS(app, resources={r"/*": {"origins": "*"}})

url = "https://v3.football.api-sports.io/leagues"
payload={}
headers = {
  'x-rapidapi-key': 'XxXxXxXxXxXxXxXxXxXxXxXx',
  'x-rapidapi-host': 'v3.football.api-sports.io'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

