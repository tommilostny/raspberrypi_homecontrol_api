import json
from flask_restful import Resource


def fetch_color_database():
    with open("data/colors.json") as f:
        return json.load(f)


class ColorDatabase(Resource):
    def get(self):
        return fetch_color_database()
