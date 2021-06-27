import json

from flask_restful import Resource
from tinytuya import BulbDevice

from utils import clamp_color, clamp_value, get_tuya_power_status


def lamp_init():
    with open("data/lamp.json") as f:
        tuya_data = json.load(f)
    bulb1 = BulbDevice(tuya_data["device_id"], tuya_data["ip"], tuya_data["local_key"])
    bulb1.set_version(3.3)
    return bulb1


lamp = lamp_init()


def set_lamp_power(status:str):
    if status == "on":
        lamp.turn_on()
    elif status == "off":
        lamp.turn_off()
    else:
        if get_tuya_power_status(lamp, 1) == "on":
            lamp.turn_off()
        else:
            lamp.turn_on()
        return { "message": "Lamp toggled." }
    return { "message": f"Lamp turned {status}." }


def set_lamp_color(red:int, green:int, blue:int):
    red, green, blue = clamp_color(red, green, blue)
    if red == 255 and green == 255 and blue == 255:
        lamp.set_colourtemp(128)
    else:
        lamp.set_colour(red, green, blue)

    if get_tuya_power_status(lamp, 1) == "off":
        lamp.turn_on()
    
    return { "message": f"Lamp color set to ({red}, {green}, {blue})." }


def set_lamp_brightness(brightness:int):
    if lamp.status()["dps"]["2"] == "white":
        lamp.set_brightness_percentage(clamp_value(brightness, 0, 100))
        message = f"Lamp brightness set to {brightness}%."
    else:
        message = "Setting lamp brightness is only possible in white mode."
    
    if get_tuya_power_status(lamp, 1) == "off":
        lamp.turn_on()
    return { "message": message }



class LampStatus(Resource):
    def get(self):
        return lamp.status()


class LampPower(Resource):
    def get(self, status:str):
        return set_lamp_power(status)


class LampColor(Resource):
    def get(self, red:int, green:int, blue:int):
        return set_lamp_color(red, green, blue)


class LampBrightness(Resource):
    def get(self, brightness:int):
        return set_lamp_brightness(brightness)
