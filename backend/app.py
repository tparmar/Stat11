from flask import Flask, render_template, request
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restx import Resource, Api, fields
import requests
import os
from dotenv import load_dotenv
from datetime import datetime


#API Using: https://dashboard.api-football.com/
#API Directions/Flowchart: https://www.api-football.com/documentation-v3#section/Authentication/API-SPORTS-Account

load_dotenv()

api_key = str(os.getenv('API_KEY'))

app = Flask(__name__)

api= Api(app, title='Stat11', description="API for Stat11 app")
cors = CORS(app, resources={r"/*": {"origins": "*"}})

payload={}
headers = {
  'x-rapidapi-key': api_key,
  'x-rapidapi-host': 'v3.football.api-sports.io'
}

ns_getLeagues = api.namespace('get-leagues',
                              description='Get the leagues')

leagues_id = [39, 140, 135, 78, 61, 2] #Prem, La liga, Serie A, Bundesliga, Ligue One, UCL
#response = requests.request("GET", url, headers=headers, data=payload)

#print(response.text)

leagues_url = "https://v3.football.api-sports.io/leagues"
fixtures_url = "https://v3.football.api-sports.io/fixtures"


league_model = api.model('League', {
    'id': fields.Integer,
    'name': fields.String,
    'country': fields.String,
    'logo': fields.String,
    'flag': fields.String,
    'fixtures_today': fields.List(fields.Raw)  # Raw because fixture details are nested/dynamic
})

headers = {
  'x-rapidapi-key': api_key,
  'x-rapidapi-host': 'v3.football.api-sports.io'
}


# 

@ns_getLeagues.route('/')
class GetLeagues(Resource):
    @api.response(200, 'Success')
    @api.marshal_list_with(league_model)
    def get(self):

        uri = "https://api.sportmonks.com/v3/football/fixtures"
        params = {
            "api_token": str(os.getenv("API_KEY_MONK"))
        }

        res = requests.get(uri, params=params)
        print(res.text)
        return res.text

if __name__ == '__main__':
    app.run(debug=True)