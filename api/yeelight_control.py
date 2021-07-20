from time import sleep

from flask_restful import Resource
from yeelight import Bulb
from yeelight.main import BulbException

from utils import clamp_color, clamp_value

yeelight_bulb = Bulb("192.168.1.189", auto_on=True)


def get_yeelight_status():
    try:
        properties = yeelight_bulb.get_properties()
    except BulbException:
        sleep(0.1)
        return get_yeelight_status()
    
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


def set_yeelight_power(status:str):
    try:
        if status == "on":
            yeelight_bulb.turn_on()
        elif status == "off":
            yeelight_bulb.turn_off()
        else:
            yeelight_bulb.toggle()
            return { "message": "Yeelight toggled." }
        return { "message": f"Yeelight turned {status}." }

    except BulbException:
        sleep(0.1)
        return set_yeelight_power(status)


def set_yeelight_color(red:int, green:int, blue:int):
    red, green, blue = clamp_color(red, green, blue)
    try:
        if red == 255 and green == 255 and blue == 255:
            yeelight_bulb.set_color_temp(3500)
        else:
            yeelight_bulb.set_rgb(red, green, blue)

        return { "message": f"Yeelight color set to ({red}, {green}, {blue})." }
    
    except BulbException:
        sleep(0.1)
        return set_yeelight_color(red, green, blue)


def set_yeelight_brightness(brightness:int):
    brightness = clamp_value(brightness, 0, 100)
    try:
        yeelight_bulb.set_brightness(brightness)
        return { "message": f"Yeelight brightness set to {brightness}%." }
    except BulbException:
        sleep(0.1)
        return set_yeelight_brightness(brightness)


def set_yeelight_temperature(temperature:int):
    temperature = clamp_value(temperature, 1700, 6500)
    try:
        yeelight_bulb.set_color_temp(temperature)
        return { "message": "Yeelight color temperature set to " + str(temperature) + "K." }
    
    except BulbException:
        sleep(0.1)
        return set_yeelight_temperature(temperature)


def set_yeelight_hue_saturation(hue:int, saturation:int):
    hue = clamp_value(hue, 0, 359)
    saturation = clamp_value(saturation, 0, 100)
    try:
        yeelight_bulb.set_hsv(hue, saturation)
        return { "message": "Yeelight hue and saturation updated" }
    except BulbException:
        sleep(0.1)
        return set_yeelight_hue_saturation(hue, saturation)


class YeelightStatus(Resource):
    def get(self):
        return get_yeelight_status()


class YeelightPower(Resource):
    def get(self, status:str):
        return set_yeelight_power(status)


class YeelightColor(Resource):
    def get(self, red:int, green:int, blue:int):
        return set_yeelight_color(red, green, blue)


class YeelightBrightness(Resource):
    def get(self, brightness:int):
        return set_yeelight_brightness(brightness)


class YeelightTemperature(Resource):
    def get(self, temperature:int):
        return set_yeelight_temperature(temperature)


class YeelightHueSaturation(Resource):
    def get(self, hue:int, saturation:int):
        return set_yeelight_hue_saturation(hue, saturation)
