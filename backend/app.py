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

@ns_getLeagues.route('/')
class GetLeagues(Resource):
    @api.response(200, 'Success')
    @api.marshal_list_with(league_model)
    def get(self):
        today = datetime.now().strftime('%Y-%m-%d')

        # 1. Get all leagues
        leagues_response = requests.get(leagues_url, headers=headers)
        all_leagues = leagues_response.json()['response']

        output = []

        for item in all_leagues:
            league = item['league']
            if league['id'] in leagues_id:
                # 2. Get fixtures for this league
                params = {
                    'league': league['id'],
                    'date': today
                }
                fixtures_response = requests.get(fixtures_url, headers=headers, params=params)
                fixtures = fixtures_response.json().get('response', [])

                # Optional: simplify fixture data if needed
                simplified_fixtures = []
                for f in fixtures:
                    simplified_fixtures.append({
                        'teams': {
                            'home': f['teams']['home']['name'],
                            'away': f['teams']['away']['name'],
                        },
                        'time': f['fixture']['date'],
                        'status': f['fixture']['status']['short'],
                        'venue': f['fixture']['venue']['name'],
                    })

                output.append({
                    'id': league['id'],
                    'name': league['name'],
                    'country': item['country']['name'],
                    'logo': league['logo'],
                    'flag': item['country'].get('flag', ''),
                    'fixtures_today': simplified_fixtures
                })

        print(output)

        return output

if __name__ == '__main__':
    app.run(debug=True)