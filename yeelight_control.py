#### Yeelight control endpoint ####
from flask_restful import Resource
from yeelight import Bulb
from time import sleep

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
        return "Yeelight bulb is " + status

class YeelightBrightness(Resource):
    def get(self, brightness):
        bulb.set_brightness(brightness)
        return "Yeelight brightness se to " + str(brightness) + "%."

def is_ok_color(color):
    if color >= 0 and color <= 255:
        return True
    else:
        return False

class YeelightColor(Resource):
    def get(self, r, g, b):
        if is_ok_color(r) and is_ok_color(g) and is_ok_color(b):
            bulb.set_rgb(r, g, b)
            if r == 255 and g == 255 and b == 255:
                bulb.set_color_temp(4000)
            return "Yeelight color set to rgb(" + str(r) + ", " + str(g) + ", " + str(b) + ")."
        else:
            return "Bad color...", 400

class YeelightTemperature(Resource):
    def get(self, temperature):
        if temperature >= 1700 and temperature <= 6500: #is a safe temperature
            bulb.set_color_temp(temperature)
            return "Yeelight color temperature set to " + str(temperature) + "K."
        else:
            return "Bad temperature: " + str(temperature), 400
#### End of Yeelight control endpoint ####