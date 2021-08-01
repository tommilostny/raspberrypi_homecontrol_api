from time import sleep

from flask_restful import Resource
from yeelight import Bulb
from yeelight.main import BulbException

from utils import clamp_color, clamp_value


class Yeelight:
    bulb = Bulb("192.168.1.189", auto_on = True)

    def get_status(self):
        try:
            properties = self.bulb.get_properties()
        except BulbException:
            sleep(0.5)
            return self.get_status()
        
        if properties["color_mode"] == "2": #white
            properties["color"] = { "red": 255, "green": 255, "blue": 255 }
        else:
            rgb = int(properties["rgb"])
            properties["color"] = {
                "red": (rgb & 0xFF0000) >> 16,
                "green": (rgb & 0x00FF00) >> 8,
                "blue": rgb & 0x0000FF
            }
        return properties


    def set_power(self, status:str):
        try:
            if status == "on":
                self.bulb.turn_on()
            elif status == "off":
                self.bulb.turn_off()
            else:
                self.bulb.toggle()
                return { "message": "Yeelight toggled." }
            return { "message": f"Yeelight turned {status}." }

        except BulbException:
            sleep(0.5)
            return self.set_power(status)


    def set_color(self, red:int, green:int, blue:int):
        red, green, blue = clamp_color(red, green, blue)
        try:
            if red == 255 and green == 255 and blue == 255:
                self.bulb.set_color_temp(3500)
            else:
                self.bulb.set_rgb(red, green, blue)

            return { "message": f"Yeelight color set to ({red}, {green}, {blue})." }
        
        except BulbException:
            sleep(0.5)
            return self.set_color(red, green, blue)


    def set_brightness(self, brightness:int):
        brightness = clamp_value(brightness, 0, 100)
        try:
            self.bulb.set_brightness(brightness)
            return { "message": f"Yeelight brightness set to {brightness}%." }
        except BulbException:
            sleep(0.5)
            return self.set_brightness(brightness)


    def set_temperature(self, temperature:int):
        temperature = clamp_value(temperature, 1700, 6500)
        try:
            self.bulb.set_color_temp(temperature)
            return { "message": "Yeelight color temperature set to " + str(temperature) + "K." }
        
        except BulbException:
            sleep(0.5)
            return self.set_temperature(temperature)


    def set_hue_saturation(self, hue:int, saturation:int):
        hue = clamp_value(hue, 0, 359)
        saturation = clamp_value(saturation, 0, 100)
        try:
            self.bulb.set_hsv(hue, saturation)
            return { "message": "Yeelight hue and saturation updated" }
        except BulbException:
            sleep(0.5)
            return self.set_hue_saturation(hue, saturation)


class YeelightStatus(Resource):
    def get(self):
        return Yeelight().get_status()


class YeelightPower(Resource):
    def get(self, status:str):
        return Yeelight().set_power(status)


class YeelightColor(Resource):
    def get(self, red:int, green:int, blue:int):
        return Yeelight().set_color(red, green, blue)


class YeelightBrightness(Resource):
    def get(self, brightness:int):
        return Yeelight().set_brightness(brightness)


class YeelightTemperature(Resource):
    def get(self, temperature:int):
        return Yeelight().set_temperature(temperature)


class YeelightHueSaturation(Resource):
    def get(self, hue:int, saturation:int):
        return Yeelight().set_hue_saturation(hue, saturation)
