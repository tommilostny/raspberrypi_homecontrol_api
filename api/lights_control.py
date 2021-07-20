from os.path import exists
from threading import Thread
from typing import List

from flask_restful import Resource

from color_db import fetch_color_database
from lamp import set_lamp_brightness, set_lamp_color, set_lamp_power
from led_strip import strip
from yeelight_control import (get_yeelight_status, set_yeelight_brightness,
                              set_yeelight_color, set_yeelight_power)


class LightsPower(Resource):
    def get(self, status):
        threads:List[Thread] = [
            Thread(target=set_lamp_power, args=[status]),
            Thread(target=set_yeelight_power, args=[status]),
            #Thread(target=strip.control_power, args=[status])
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        return { "message": f"Lights turned {status}." }


def set_lights_color(r, g, b):
    threads:List[Thread] = [
        Thread(target=set_lamp_color, args=[r, g, b]),
        Thread(target=set_yeelight_color, args=[r, g, b]),
        #Thread(target=strip.set_color, args=[r, g, b])
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return { "message": f"Lights color set to ({r}, {g}, {b})." }


class LightsColorByRGB(Resource):
    def get(self, r, g, b):
        set_lights_color(r, g, b)


class LightsColorByName(Resource):
    def get(self, color_name):
        for x in fetch_color_database():
            if x["name"] == color_name:
                set_lights_color(x["color"]["red"], x["color"]["green"], x["color"]["blue"])
                return { "message": "Found and set color: " + color_name }
        return { "message": "Color " + str(color_name) + " not found." }, 404


class LightsColorCycle(Resource):
    def get(self):
        if exists("data/color_cycle_index"):
            with open("data/color_cycle_index", "r") as file:
                color_db_index = int(file.readline())
        else:
            color_db_index = 0
            with open("data/color_cycle_index", "x") as file:
                file.write("0")

        color_db = fetch_color_database()
        color = color_db[color_db_index]
        set_lights_color(color["color"]["red"], color["color"]["green"], color["color"]["blue"])

        with open("data/color_cycle_index", "w") as file:
            file.write(str((color_db_index + 1) % len(color_db)))

        return { "message": f"Yeelight set to color {color}" }


def set_lights_brightness(brightness:int):
    threads:List[Thread] = [
        Thread(target=set_lamp_brightness, args=[brightness]),
        Thread(target=set_yeelight_brightness, args=[brightness]),
        #Thread(target=strip.set_brightness, args=[brightness])
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return { "message": f"Lights brightness set to {brightness}%." }


class LightsBrightness(Resource):
    def get(self, brightness):
        return set_lights_brightness(brightness)


class LightsBrightnessCycle(Resource):
    def get(self, lower:int, upper:int):
        current = int(get_yeelight_status()["bright"])

        if abs(current - lower) > abs(current - upper):
            return set_lights_brightness(lower)
        else:
            return set_lights_brightness(upper)
