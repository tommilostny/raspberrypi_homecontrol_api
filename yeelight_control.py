#### Yeelight control endpoint ####
import json

from flask_restful import Resource
from yeelight import Bulb

bulb = Bulb("192.168.1.189", auto_on=True)

class YeelightStatus(Resource):
    def get(self):
        return bulb.get_properties()

class YeelightPower(Resource):
    def get(self, status):
        if status == "on":
            bulb.turn_on()
        elif status == "off":
            bulb.turn_off()
        else:
            bulb.toggle()
            status = "toggled"
        return { "message": "Yeelight bulb is " + status }

class YeelightBrightness(Resource):
    def get(self, brightness):
        if brightness >= 0 and brightness <= 100:
            bulb.set_brightness(brightness)
            return { "message": "Yeelight brightness se to " + str(brightness) + "%." }
        else:
            return { "message": "Bad brightness: " + str(brightness) }, 400

def is_ok_color(color):
    return (color >= 0 and color <= 255)

def set_color(r, g, b):
    bulb.set_rgb(r, g, b)
    if r == 255 and g == 255 and b == 255:
        bulb.set_color_temp(4000)

class YeelightColorRGB(Resource):
    def get(self, r, g, b):
        if is_ok_color(r) and is_ok_color(g) and is_ok_color(b):
            set_color(r, g, b)
            return { "message": "Yeelight color set to rgb(" + str(r) + ", " + str(g) + ", " + str(b) + ")." }
        else:
            return { "message": "Bad color..." }, 400

class YeelightColorName(Resource):
    def get(self, color_name):
        for x in fetch_color_database():
            if x["name"] == color_name:
                set_color(x["color"]["red"], x["color"]["green"], x["color"]["blue"])
                return { "message": "Found and set color: " + color_name }
        return { "message": "Color " + str(color_name) + " not found." }, 404

class YeelightTemperature(Resource):
    def get(self, temperature):
        if temperature >= 1700 and temperature <= 6500: #is a safe temperature
            bulb.set_color_temp(temperature)
            return { "message": "Yeelight color temperature set to " + str(temperature) + "K." }
        else:
            return { "message": "Bad temperature: " + str(temperature) }, 400

class YeelightHueSaturation(Resource):
    def get(self, hue, saturation):
        if hue < 0 or hue > 359:
            return { "message": "Bad hue: " + str(hue) }, 400
        elif saturation < 0 or saturation > 100:
            return { "message": "Bad saturation: " + str(saturation) }, 400
        else:
            bulb.set_hsv(hue, saturation)
            return { "message": "Yeelight hue and saturation updated" }

def fetch_color_database():
    with open("data/colors.json") as f:
        return json.load(f)

class ColorDatabase(Resource):
    def get(self):
        return fetch_color_database()
#### End of Yeelight control endpoint ####
