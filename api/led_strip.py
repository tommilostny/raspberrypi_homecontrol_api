import json
from os.path import exists

from flask_restful import Resource
from gpiozero import PWMLED, RGBLED

from utils import clamp_value, clamp_color


class LedStrip:
    status_file = "data/ledstrip.json"

    def __init__(self, red_pin:int = 24, green_pin:int = 25, blue_pin:int = 20, white_pin:int = 18):
        self.rgb = RGBLED(red_pin, green_pin, blue_pin)
        self.white = PWMLED(white_pin)
        self.rgb.off()
        self.white.off()

        if exists(self.status_file):
            with open(self.status_file, "r") as file:
                self.status = json.load(file)
            
            if self.status["power"] == "on":
                self.set_leds_by_mode()
        else:
            self.status = {
                "power": "off",
                "mode" : "white",
                "brightness" : 100,
                "color" : {
                    "red" : 255,
                    "green" : 255,
                    "blue" : 255
                }
            }
            with open(self.status_file, "x") as file:
                json.dump(self.status, file)


    def _save_status(self):
        with open(self.status_file, "w") as file:
            json.dump(self.status, file)


    def _brightness_to_float(self):
        return self.status["brightness"] / 100


    def set_rgb_leds(self):
        self.rgb.value = [(x / 255) * self._brightness_to_float() for x in self.status["color"].values()]
        self._save_status()

    
    def set_white_led(self):
        self.white.value = self._brightness_to_float()
        self._save_status()

    
    def set_leds_by_mode(self):
        if self.status["mode"] == "white":
            self.set_white_led()
        else:
            self.set_rgb_leds()


    def set_power(self, status:str):
        if status == "on":
            self.status["power"] = "on"
            if self.status["mode"] == "white":
                self.set_white_led()
                return { "message": "White LEDs turned on." }
            else:
                self.set_rgb_leds()
                return { "message": "RGB LEDs turned on." }

        elif status == "off":
            self.status["power"] = "off"
            if self.status["mode"] == "white":
                self.white.off()
                self._save_status()
                return { "message": "White LEDs turned off." }
            else:
                self.rgb.off()
                self._save_status()
                return { "message": "RGB LEDs turned off." }

        else:
            if self.status["mode"] == "white":
                self.status["power"] = "off" if self.white.is_active else "on"
                if self.white.is_active:
                    self.white.off()
                    self._save_status()
                else:
                    self.set_white_led()
                return { "message": "White LEDs toggled." }
            else:
                self.status["power"] = "off" if self.rgb.is_active else "on"
                if self.rgb.is_active:
                    self.rgb.off()
                    self._save_status()
                else:
                    self.set_rgb_leds()
                return { "message": "RGB LEDs toggled." }


    def set_color(self, red:int, green:int, blue:int):
        red, green, blue = clamp_color(red, green, blue)
        self.status["power"] = "on"

        if red == 255 and green == 255 and blue == 255:
            if self.status["mode"] == "white":
                self.set_white_led()
            else:
                self.rgb.off()
                self.status["mode"] = "white"
                self.status["color"] = { "red":255, "green":255, "blue":255 }
                self.set_white_led()
        else:
            self.status["color"] = { "red":red, "green":green, "blue":blue }
            self.white.off()
            self.status["mode"] = "rgb"
            self.set_rgb_leds()


    def set_brightness(self, brightness:int):
        brightness = clamp_value(brightness, 0, 100)
        self.status["brightness"] = brightness
        self.status["power"] = "on"
        self.set_leds_by_mode()
        return { "message": f"LEDs brightness set to {brightness}%." }


strip = LedStrip()


class LedStripStatus(Resource):
    def get(self):
        return strip.status


class LedStripPower(Resource):
    def get(self, status:str):
        return strip.set_power(status)


class LedStripColor(Resource):
    def get(self, red:int, green:int, blue:int):
        strip.set_color(red, green, blue)


class LedStripBrightness(Resource):
    def get(self, brightness:int):
        return strip.set_brightness(brightness)
