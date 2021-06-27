import json
from time import sleep

from flask_restful import Resource
from yeelight.main import BulbException

from led_strip import strip
from lamp import get_lamp_mode, lamp
from multiplug import get_tuya_power_status
from yeelight_control import yeelight_bulb


def set_lights_power(status):
    try:
        if status == "on":
            yeelight_bulb.turn_on()
            lamp.turn_on()
        elif status == "off":
            yeelight_bulb.turn_off()
            lamp.turn_off()
        else:
            power = get_tuya_power_status(lamp, 1)
            if power == "on":
                lamp.turn_off()
            else:
                lamp.turn_on()
            yeelight_bulb.toggle()
            status = "toggled"

        strip.control_power(status)
        return { "message": "Lights are " + status }

    except BulbException:
        sleep(0.1)
        return set_lights_power(status)


class LightsPower(Resource):
    def get(self, status):
        return set_lights_power(status)


def set_lights_brightness(brightness):
    try:
        yeelight_bulb.set_brightness(brightness)
        if get_lamp_mode() == "white":
            lamp.set_brightness_percentage(brightness)
            #lamp.set_brightness(int(2.8 * brightness - 25))

        strip.set_brightness(brightness)
        return { "message": "Lights brightness set to " + str(brightness) + "%." }
    
    except BulbException:
        sleep(0.1)
        return set_lights_brightness(brightness)


class LightsBrightness(Resource):
    def get(self, brightness):
        if brightness >= 0 and brightness <= 100:
            return set_lights_brightness(brightness)
        else:
            return { "message": "Bad brightness: " + str(brightness) }, 400


class LightsBrightnessCycle(Resource):
    def get(self, lower:int, upper:int):
        current = int(yeelight_bulb.get_properties()["bright"])

        if abs(current - lower) > abs(current - upper):
            return set_lights_brightness(lower)
        else:
            return set_lights_brightness(upper)


def is_ok_color(color):
    return (color >= 0 and color <= 255)


def set_lights_color(r, g, b):
    try:
        power = get_tuya_power_status(lamp, 1)
        if power == "off":
            lamp.turn_on()

        lamp.set_colour(r, g, b)
        yeelight_bulb.set_rgb(r, g, b)
        
        if r == 255 and g == 255 and b == 255:
            yeelight_bulb.set_color_temp(3500)
            lamp.set_colourtemp(128)

        strip.set_color(r, g, b)

    except BulbException:
        sleep(0.1)
        set_lights_color(r, g, b)


class LightsColorByRGB(Resource):
    def get(self, r, g, b):
        if is_ok_color(r) and is_ok_color(g) and is_ok_color(b):
            set_lights_color(r, g, b)
            return { "message": "Yeelight color set to rgb(" + str(r) + ", " + str(g) + ", " + str(b) + ")." }
        else:
            return { "message": "Bad color..." }, 400


class LightsColorByName(Resource):
    def get(self, color_name):
        for x in fetch_color_database():
            if x["name"] == color_name:
                set_lights_color(x["color"]["red"], x["color"]["green"], x["color"]["blue"])
                return { "message": "Found and set color: " + color_name }
        return { "message": "Color " + str(color_name) + " not found." }, 404


def fetch_color_database():
    with open("data/colors.json") as f:
        return json.load(f)


class ColorDatabase(Resource):
    def get(self):
        return fetch_color_database()


color_db_index = 0


class LightsColorCycle(Resource):
    def get(self):
        global color_db_index

        color_db = fetch_color_database()
        color = color_db[color_db_index]
        set_lights_color(color["color"]["red"], color["color"]["green"], color["color"]["blue"])

        color_db_index = (color_db_index + 1) % len(color_db)
        return { "message": f"Yeelight set to color {color}" }
