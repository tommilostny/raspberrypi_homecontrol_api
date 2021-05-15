import threading

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from heater_control import *
from lcd_control import *
from led_control import *
from lights_control import *
from temperature import *
from tuya_devices import *

heater_thread_stop_event = threading.Event()
heater_thread = HeaterControlThread(heater_thread_stop_event)

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

api.add_resource(LED_Control, "/led/<int:led_num>/<string:status>")
api.add_resource(LED_Status, "/led")
api.add_resource(LED_Blink, "/led/<int:led_num>/blink/<float:interval>")
api.add_resource(RGB_LED_Color_ByName, "/led/rgb/<string:name>")
api.add_resource(RGB_LED_Color_ByRGB, "/led/rgb/<int:r>/<int:g>/<int:b>")

api.add_resource(LightsPower, "/lights/power/<string:status>")
api.add_resource(LightsBrightness, "/lights/brightness/<int:brightness>")
api.add_resource(LightsColorByRGB, "/lights/color/<int:r>/<int:g>/<int:b>")
api.add_resource(LightsColorByName, "/lights/color/<string:color_name>")
api.add_resource(LightsColorCycle, "/lights/cycle")
api.add_resource(LightsBrightnessCycle, "/lights/cycle/<int:lower>/<int:upper>")

api.add_resource(YeelightStatus, "/yeelight")
api.add_resource(YeelightTemperature, "/yeelight/temperature/<int:temperature>")
api.add_resource(YeelightHueSaturation, "/yeelight/hs/<int:hue>/<int:saturation>")

api.add_resource(ColorDatabase, "/colors")

api.add_resource(Temperature, "/temperature")
api.add_resource(LcdControl, "/heater_lcd/<int:state>")
api.add_resource(LcdMessage, "/lcd_message/<string:message>/<int:line>")
api.add_resource(TemperatureLog, "/temp_log")
api.add_resource(TemperatureThreshold, "/temp_threshold/<string:period>/<float:threshold>")

api.add_resource(MultiPlugControl, "/multiplug/<string:device_name>/<string:power_status>")
api.add_resource(MultiPlugListDevices, "/multiplug/list")
api.add_resource(MultiPlugStatus, "/multiplug/status")

api.add_resource(LampStatus, "/lamp/status")

if __name__ == "__main__":
    heater_thread.start()
    app.run(debug=True, host="0.0.0.0", use_reloader=False, ssl_context=('cert.pem', 'key.pem'))
    heater_thread_stop_event.set()
