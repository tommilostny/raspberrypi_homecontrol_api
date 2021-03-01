#### Yeelight controls ####
import json

from flask_restful import Resource
from yeelight import Bulb
from yeelight.main import BulbException
from time import sleep

bulb = Bulb("192.168.1.189", auto_on=True)

#### Bulb status endpoint ####
def getBulbStatus():
    try:
        return bulb.get_properties()
    except BulbException:
        sleep(0.1)
        return getBulbStatus()

class YeelightStatus(Resource):
    def get(self):
        return getBulbStatus()
#### End of bulb status endpoint ####

#### Bulb power endpoint ####
def setBulbPower(status):
    try:
        if status == "on":
            bulb.turn_on()
        elif status == "off":
            bulb.turn_off()
        else:
            bulb.toggle()
            status = "toggled"
        return { "message": "Yeelight bulb is " + status }
    except BulbException:
        sleep(0.1)
        return setBulbPower(status)

class YeelightPower(Resource):
    def get(self, status):
        return setBulbPower(status)
#### End of bulb power endpoint ####

#### Bulb brightness endpoint ####
def setBulbBrightness(brightness):
    try:
        bulb.set_brightness(brightness)
        return { "message": "Yeelight brightness se to " + str(brightness) + "%." }
    except BulbException:
        sleep(0.1)
        return setBulbBrightness(brightness)
class YeelightBrightness(Resource):
    def get(self, brightness):
        if brightness >= 0 and brightness <= 100:
            return setBulbBrightness(brightness)
        else:
            return { "message": "Bad brightness: " + str(brightness) }, 400
#### End of bulb brightness endpoint ####

#### Bulb color by RGB or name endpoint ####
def is_ok_color(color):
    return (color >= 0 and color <= 255)

def set_color(r, g, b):
    try:
        bulb.set_rgb(r, g, b)
        if r == 255 and g == 255 and b == 255:
            bulb.set_color_temp(4000)
    except BulbException:
        sleep(0.1)
        set_color(r, g, b)

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
#### End of bulb color by RGB and name endpoint ####

#### Bulb white temperure endpoint ####
def setBulbTemperature(temperature):
    try:
        bulb.set_color_temp(temperature)
        return { "message": "Yeelight color temperature set to " + str(temperature) + "K." }
    except BulbException:
        sleep(0.1)
        return setBulbTemperature(temperature)

class YeelightTemperature(Resource):
    def get(self, temperature):
        if temperature >= 1700 and temperature <= 6500: #is a safe temperature
            return setBulbTemperature(temperature)
        else:
            return { "message": "Bad temperature: " + str(temperature) }, 400
#### End of bulb white temperure endpoint ####

#### Bulb hue and saturation endpoint ####
def setHueAndSaturation(hue, saturation):
    try:
        bulb.set_hsv(hue, saturation)
        return { "message": "Yeelight hue and saturation updated" }
    except BulbException:
        sleep(0.1)
        return setHueAndSaturation(hue, saturation)

class YeelightHueSaturation(Resource):
    def get(self, hue, saturation):
        if hue < 0 or hue > 359:
            return { "message": "Bad hue: " + str(hue) }, 400
        elif saturation < 0 or saturation > 100:
            return { "message": "Bad saturation: " + str(saturation) }, 400
        else:
            return setHueAndSaturation(hue, saturation)            
#### End of bulb hue and saturation endpoint ####

#### Color database (now from file TODO?) ####
def fetch_color_database():
    with open("data/colors.json") as f:
        return json.load(f)

class ColorDatabase(Resource):
    def get(self):
        return fetch_color_database()
#### End of color database ####