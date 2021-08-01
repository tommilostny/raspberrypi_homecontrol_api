import json

from flask_restful import Resource
from tinytuya import BulbDevice

from utils import clamp_color, clamp_value, get_tuya_power_status


class Lamp:
    def __init__(self):
        with open("data/lamp.json") as f:
            tuya_data = json.load(f)
        self.bulb = BulbDevice(tuya_data["device_id"], tuya_data["ip"], tuya_data["local_key"])
        self.bulb.set_version(3.3)


    def get_status(self):
        state = self.bulb.state()
        r, g, b = self.bulb.colour_rgb() if state["mode"] == "colour" else (255, 255, 255)
        return {
            "power": "on" if state["is_on"] else "off",
            "brightness": int((state["brightness"] / 255) * 100),
            "color": {
                "red": r, "green": g, "blue": b
            }
        }


    def set_power(self, status:str):
        if status == "on":
            self.bulb.turn_on()
        elif status == "off":
            self.bulb.turn_off()
        else:
            if get_tuya_power_status(self.bulb, 1) == "on":
                self.bulb.turn_off()
            else:
                self.bulb.turn_on()
            return { "message": "Lamp toggled." }
        return { "message": f"Lamp turned {status}." }


    def set_color(self, red:int, green:int, blue:int):
        red, green, blue = clamp_color(red, green, blue)
        if red == 255 and green == 255 and blue == 255:
            self.bulb.set_colourtemp(128)
        else:
            self.bulb.set_colour(red, green, blue)

        if get_tuya_power_status(self.bulb, 1) == "off":
            self.bulb.turn_on()
        
        return { "message": f"Lamp color set to ({red}, {green}, {blue})." }


    def set_brightness(self, brightness:int):
        if self.bulb.status()["dps"]["2"] == "white":
            self.bulb.set_brightness_percentage(clamp_value(brightness, 0, 100))
            message = f"Lamp brightness set to {brightness}%."
        else:
            message = "Setting lamp brightness is only possible in white mode."
        
        if get_tuya_power_status(self.bulb, 1) == "off":
            self.bulb.turn_on()
        return { "message": message }



class LampStatus(Resource):
    def get(self):
        return Lamp().get_status()


class LampPower(Resource):
    def get(self, status:str):
        return Lamp().set_power(status)


class LampColor(Resource):
    def get(self, red:int, green:int, blue:int):
        return Lamp().set_color(red, green, blue)


class LampBrightness(Resource):
    def get(self, brightness:int):
        return Lamp().set_brightness(brightness)
