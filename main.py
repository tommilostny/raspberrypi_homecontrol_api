#Library imports
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

#Local modules imports
import led_control as lc
import yeelight_control as yc
import temperature as t
import lcd_control as lcdc

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

api.add_resource(lc.LED_Control, "/led/<int:led_num>/<string:status>")
api.add_resource(lc.LED_Status, "/led")
api.add_resource(lc.LED_Blink, "/led/<int:led_num>/blink/<float:interval>")

api.add_resource(yc.YeelightPower, "/yeelight/power/<string:status>")
api.add_resource(yc.YeelightBrightness, "/yeelight/brightness/<int:brightness>")
api.add_resource(yc.YeelightColorRGB, "/yeelight/color/<int:r>/<int:g>/<int:b>")
api.add_resource(yc.YeelightStatus, "/yeelight")
api.add_resource(yc.YeelightTemperature, "/yeelight/temperature/<int:temperature>")
api.add_resource(yc.YeelightHueSaturation, "/yeelight/hs/<int:hue>/<int:saturation>")
api.add_resource(yc.ColorDatabase, "/colors")
api.add_resource(yc.YeelightColorName, "/yeelight/color/<string:color_name>")

api.add_resource(t.Temperature, "/temperature")

api.add_resource(lcdc.LcdPrint, "/lcd/<string:message>/<int:line>")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
