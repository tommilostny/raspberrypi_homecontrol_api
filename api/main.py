import threading
from subprocess import Popen

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from color_db import *
from heater_control import *
from lamp import *
from lcd_control import *
from led_control import *
from led_strip import *
from lights_control import *
from multiplug import *
from temperature import *
from weather import *
from yeelight_control import *

blazor_process = Popen(["dotnet", "run", "-p", "../RpiHomeHub.BlazorWeb/RpiHomeHub.BlazorWeb.csproj"])

heater_thread_stop_event = threading.Event()
heater_thread = HeaterControlThread(heater_thread_stop_event)

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources = { r"/*": {"origins": "*" } })

api.add_resource(LED_Control, "/led/<int:led_num>/<string:status>")
api.add_resource(LED_Status, "/led")
api.add_resource(LED_Blink, "/led/<int:led_num>/blink/<float:interval>")
api.add_resource(RGB_LED_Color_ByName, "/led/rgb/<string:name>")
api.add_resource(RGB_LED_Color_ByRGB, "/led/rgb/<int:r>/<int:g>/<int:b>")

api.add_resource(LightsPower, "/lights/<string:status>")
api.add_resource(LightsBrightness, "/lights/<int:brightness>")
api.add_resource(LightsColorByRGB, "/lights/<int:r>/<int:g>/<int:b>")
api.add_resource(LightsColorByName, "/lights/color/<string:color_name>")
api.add_resource(LightsColorCycle, "/lights/color_cycle/<string:direction>")
api.add_resource(LightsBrightnessCycle, "/lights/brightness_cycle/<int:lower>/<int:upper>")

api.add_resource(ColorDatabase, "/colors")

api.add_resource(Temperature, "/temperature")
api.add_resource(LcdControl, "/heater_lcd/<int:state>")
api.add_resource(LcdMessage, "/lcd_message/<string:message>/<int:line>")
api.add_resource(TemperatureLog, "/temp_log")
api.add_resource(TemperatureThreshold, "/temp_threshold/<string:period>/<float:threshold>")

api.add_resource(MultiPlugControl, "/multiplug/<string:device_name>/<string:power_status>")
api.add_resource(MultiPlugListDevices, "/multiplug/list")
api.add_resource(MultiPlugStatus, "/multiplug/status")

api.add_resource(LampStatus, "/lamp")
api.add_resource(LampPower, "/lamp/<string:status>")
api.add_resource(LampColor, "/lamp/<int:red>/<int:green>/<int:blue>")
api.add_resource(LampBrightness, "/lamp/<int:brightness>")

api.add_resource(LedStripStatus, "/ledstrip")                                   #status
api.add_resource(LedStripPower, "/ledstrip/<string:status>")                    #power
api.add_resource(LedStripColor, "/ledstrip/<int:red>/<int:green>/<int:blue>")   #color
api.add_resource(LedStripBrightness, "/ledstrip/<int:brightness>")              #brightness

api.add_resource(YeelightStatus, "/yeelight")
api.add_resource(YeelightPower, "/yeelight/<string:status>")
api.add_resource(YeelightColor, "/yeelight/<int:red>/<int:green>/<int:blue>")
api.add_resource(YeelightBrightness, "/yeelight/<int:brightness>")
api.add_resource(YeelightTemperature, "/yeelight/temperature/<int:temperature>")
api.add_resource(YeelightHueSaturation, "/yeelight/hs/<int:hue>/<int:saturation>")

api.add_resource(Weather, "/weather")

if __name__ == "__main__":
    heater_thread.start()
    app.run(debug = True, host = "0.0.0.0", use_reloader = False)#, ssl_context = ("cert.pem", "key.pem"))
    heater_thread_stop_event.set()
    blazor_process.terminate()
