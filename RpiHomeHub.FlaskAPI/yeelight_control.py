from time import sleep

from flask_restful import Resource
from yeelight import Bulb
from yeelight.main import BulbException


yeelight_bulb = Bulb("192.168.1.189", auto_on=True)


def get_yeelight_status():
    try:
        return yeelight_bulb.get_properties()
    except BulbException:
        sleep(0.1)
        return get_yeelight_status()


class YeelightStatus(Resource):
    def get(self):
        return get_yeelight_status()


def set_lights_temperature(temperature):
    try:
        yeelight_bulb.set_color_temp(temperature)
        return { "message": "Yeelight color temperature set to " + str(temperature) + "K." }
    except BulbException:
        sleep(0.1)
        return set_lights_temperature(temperature)


class YeelightTemperature(Resource):
    def get(self, temperature):
        if temperature >= 1700 and temperature <= 6500: #is a safe temperature
            return set_lights_temperature(temperature)
        else:
            return { "message": "Bad temperature: " + str(temperature) }, 400


def set_yeelight_hue_saturation(hue, saturation):
    try:
        yeelight_bulb.set_hsv(hue, saturation)
        return { "message": "Yeelight hue and saturation updated" }
    except BulbException:
        sleep(0.1)
        return set_yeelight_hue_saturation(hue, saturation)


class YeelightHueSaturation(Resource):
    def get(self, hue, saturation):
        if hue < 0 or hue > 359:
            return { "message": "Bad hue: " + str(hue) }, 400
        elif saturation < 0 or saturation > 100:
            return { "message": "Bad saturation: " + str(saturation) }, 400
        else:
            return set_yeelight_hue_saturation(hue, saturation)
