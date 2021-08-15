import json

from requests import get
from flask_restful import Resource


class Weather(Resource):
    def __init__(self):
        with open("data/weather_api.json", "r") as file:
            info = json.load(file)

        for key, value in info.items():
            setattr(self, key, value)

        super().__init__()


    def get(self):
        request = get(f"https://api.openweathermap.org/data/2.5/weather?id={self.city_id}&appid={self.api_key}&units=metric")
        return request.json()
