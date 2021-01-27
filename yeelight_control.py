#### Yeelight control endpoint ####
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
            return "Yeelight color set to rgb(" + str(r) + ", " + str(g) + ", " + str(b) + ")."
        else:
            return "Bad color...", 400
#### End of Yeelight control endpoint ####