from flask import jsonify
from flask.views import MethodView
import requests
from requests.auth import HTTPBasicAuth

from requests.auth import HTTPBasicAuth
from config import CLIENT_ID,CLIENT_SECRET,API_URL

class MoviesAPI(MethodView):
    def get(self):
        '''
            This endpoint will fetch the movie list

            Response Payload:
            {
                “count”: <total number of movies>,
                “next”: <link for next page, if present>,
                “previous”: <link for previous page>,
                “data”: [
                    {
                        “title”: <title of the movie>,
                        “description”: <a description of the movie>,
                        “genres”: <a comma separated list of genres, if
                        “uuid”: <a unique uuid for the movie>
                        present>,
                    },
                    ...
                ]
            }
    
        '''
        try:
            # load_dotenv(".env")
            response = requests.get(API_URL,auth=HTTPBasicAuth(CLIENT_ID,CLIENT_SECRET))
            response.raise_for_status()
            data = response.json()
            return jsonify(data), 200
        except requests.exceptions.RequestException:
            return jsonify({'error': 'failed to fetch movies data'}), 500
