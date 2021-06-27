import json
from time import sleep

from flask_restful import Resource
from tinytuya import BulbDevice


def lamp_init():
    with open("data/lamp.json") as f:
        tuya_data = json.load(f)
    bulb1 = BulbDevice(tuya_data["device_id"], tuya_data["ip"], tuya_data["local_key"])
    bulb1.set_version(3.3)
    return bulb1


lamp = lamp_init()


def get_lamp_mode() -> str:
    try:
        data = lamp.status()
        return data["dps"]["2"]
    except:
        sleep(0.5)
        return get_lamp_mode()


class LampStatus(Resource):
    def get(self):
        try:
            return lamp.status()
        except:
            sleep(0.1)
            return self.get()
