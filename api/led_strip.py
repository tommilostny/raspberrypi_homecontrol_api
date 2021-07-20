import json
from os.path import exists

from flask_restful import Resource
from gpiozero import PWMLED, RGBLED

from utils import clamp_value, clamp_color


class LedStrip:
    status_file = "data/ledstripmode.json"

    def __init__(self, red_pin:int, green_pin:int, blue_pin:int, white_pin:int):
        self.rgb = RGBLED(red_pin, green_pin, blue_pin)
        self.white = PWMLED(white_pin)

        if exists(self.status_file):
            with open(self.status_file, "r") as file:
                self.status = json.load(file)
            
            if self.status["mode"] == "white":
                self.white.value = self.get_converted_status()
            else:
                self.rgb.value = self.get_converted_status()
        else:
            self.status = { "mode": "white", "value": 255 }
            with open(self.status_file, "x") as file:
                json.dump(self.status, file)


    def save_status(self):
        with open(self.status_file, "w") as file:
            json.dump(self.status, file)


    def get_converted_status(self):
        if self.status["mode"] == "white":
            return self.status["value"] / 255
        else:
            return [x / 255 for x in self.status["value"]]


    def control_power(self, status:str):
        mode = self.status["mode"]

        if status == "on":
            if mode == "white":
                self.white.value = self.get_converted_status()
                return { "message": "White LEDs turned on." }
            else:
                self.rgb.value = self.get_converted_status()
                return { "message": "RGB LEDs turned on." }

        elif status == "off":
            if mode == "white":
                self.white.off()
                return { "message": "White LEDs turned off." }
            else:
                self.rgb.off()
                return { "message": "RGB LEDs turned off." }

        else:
            if mode == "white":
                if self.white.is_active:
                    self.white.off()
                else:
                    self.white.value = self.get_converted_status()
                return { "message": "White LEDs toggled." }
            else:
                if self.rgb.is_active:
                    self.rgb.off()
                else:
                    self.rgb.value = self.get_converted_status()
                return { "message": "RGB LEDs toggled." }


    def set_color(self, red:int, green:int, blue:int):
        red, green, blue = clamp_color(red, green, blue)

        if red == 255 and green == 255 and blue == 255:
            if self.status["mode"] == "white":
                self.white.value = self.get_converted_status()
            else:
                self.rgb.off()
                self.white.on()
                self.status["mode"] = "white"
                self.status["value"] = 255
        else:
            self.status["mode"] = "rgb"
            self.status["value"] = [ red, green, blue ]
            self.white.off()
            self.rgb.value = (red / 255, green / 255, blue / 255)

        self.save_status()


    def set_brightness(self, brightness:int):
        brightness = clamp_value(brightness, 0, 100)
        float_value = brightness / 100

        if self.status["mode"] == "white":
            self.white.value = float_value
            self.status["value"] = int(float_value * 255)
            self.save_status()
        else:
            self.rgb.value = [(x * float_value) / 255 for x in self.status["value"]]
        
        return { "message": f"LEDs brightness set to {brightness}%." }


strip = LedStrip(24, 25, 20, 18)


class LedStripStatus(Resource):
    def get(self):
        return {
            "mode": strip.status["mode"],
            "rgbValue": [int(x * 255) for x in strip.rgb.value],
            "whiteValue": int(strip.white.value * 255)
        }


class LedStripPower(Resource):
    def get(self, status:str):
        return strip.control_power(status)


class LedStripColor(Resource):
    def get(self, red:int, green:int, blue:int):
        strip.set_color(red, green, blue)


class LedStripBrightness(Resource):
    def get(self, brightness:int):
        return strip.set_brightness(brightness)
