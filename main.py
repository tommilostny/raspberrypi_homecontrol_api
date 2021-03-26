import threading

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from heater_control import *
from led_control import *
from temperature import *
from yeelight_control import *

e = threading.Event()
heater_thread = HC_Thread(e)

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

api.add_resource(LED_Control, "/led/<int:led_num>/<string:status>")
api.add_resource(LED_Status, "/led")
api.add_resource(LED_Blink, "/led/<int:led_num>/blink/<float:interval>")
api.add_resource(RGB_LED_Color_ByName, "/led/rgb/<string:name>")
api.add_resource(RGB_LED_Color_ByRGB, "/led/rgb/<int:r>/<int:g>/<int:b>")

api.add_resource(YeelightPower, "/yeelight/power/<string:status>")
api.add_resource(YeelightBrightness, "/yeelight/brightness/<int:brightness>")
api.add_resource(YeelightColorRGB, "/yeelight/color/<int:r>/<int:g>/<int:b>")
api.add_resource(YeelightStatus, "/yeelight")
api.add_resource(YeelightTemperature, "/yeelight/temperature/<int:temperature>")
api.add_resource(YeelightHueSaturation, "/yeelight/hs/<int:hue>/<int:saturation>")
api.add_resource(ColorDatabase, "/colors")
api.add_resource(YeelightColorName, "/yeelight/color/<string:color_name>")

api.add_resource(Temperature, "/temperature")
api.add_resource(LcdControl, "/heater_lcd/<int:state>")
api.add_resource(LcdMessage, "/lcd_message/<string:message>/<int:line>")
api.add_resource(TemperatureLog, "/temp_log")
api.add_resource(TemperatureThreshold, "/temp_threshold/<string:period>/<float:threshold>")

if __name__ == "__main__":
    heater_thread.start()
    app.run(debug=True, host="0.0.0.0", use_reloader=False, ssl_context=('cert.pem', 'key.pem'))
    e.set()
