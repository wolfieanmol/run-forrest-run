import requests
from requests.exceptions import RequestException

import json


class LeaderboardHandler:
    base_url = "http://localhost:4700/api/v1/leaderboard"

    @classmethod
    def get_rank(cls, user_id):
        try:
            url = f"{cls.base_url}/rank/{user_id}"
            response = requests.get(url)
            return json.loads(response.content)
        except RequestException as e:
            return {"message": "api endpoint is down"}

    @classmethod
    def get_top_leaderboard(cls, num):
        try:
            url = f"{cls.base_url}/top/{num}"
            response = requests.get(url)
            return json.loads(response.content)
        except RequestException as e:
            return {"message": "api endpoint is down"}

    @classmethod
    def create_user(cls, user_id):
        try:
            url = f"{cls.base_url}/create-user/{user_id}"
            response = requests.put(url)
            return json.loads(response.content)
        except RequestException as e:
            return {"message": "api endpoint is down"}
