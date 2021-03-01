import threading

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

import heater_control as hc
import led_control as lc
import temperature as t
import yeelight_control as yc

e = threading.Event()
heater_thread = hc.HC_Thread(e)

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

api.add_resource(lc.LED_Control, "/led/<int:led_num>/<string:status>")
api.add_resource(lc.LED_Status, "/led")
api.add_resource(lc.LED_Blink, "/led/<int:led_num>/blink/<float:interval>")
api.add_resource(lc.RGB_LED_Color_ByName, "/led/rgb/<string:name>")
api.add_resource(lc.RGB_LED_Color_ByRGB, "/led/rgb/<int:r>/<int:g>/<int:b>")

api.add_resource(yc.YeelightPower, "/yeelight/power/<string:status>")
api.add_resource(yc.YeelightBrightness, "/yeelight/brightness/<int:brightness>")
api.add_resource(yc.YeelightColorRGB, "/yeelight/color/<int:r>/<int:g>/<int:b>")
api.add_resource(yc.YeelightStatus, "/yeelight")
api.add_resource(yc.YeelightTemperature, "/yeelight/temperature/<int:temperature>")
api.add_resource(yc.YeelightHueSaturation, "/yeelight/hs/<int:hue>/<int:saturation>")
api.add_resource(yc.ColorDatabase, "/colors")
api.add_resource(yc.YeelightColorName, "/yeelight/color/<string:color_name>")

api.add_resource(hc.Temperature, "/temperature")
api.add_resource(hc.LcdControl, "/heater_lcd/<int:state>")
api.add_resource(hc.LcdMessage, "/lcd_message/<string:message>/<int:line>")
api.add_resource(hc.TemperatureLog, "/temp_log")
api.add_resource(hc.TemperatureThreshold, "/temp_threshold/<string:period>/<float:threshold>")

if __name__ == "__main__":
    heater_thread.start()
    app.run(debug=True, host="0.0.0.0", use_reloader=False, ssl_context=('cert.pem', 'key.pem'))
    e.set()
