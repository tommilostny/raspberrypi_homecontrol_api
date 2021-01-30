#Library imports
from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS

#Local modules imports
from testfiles import helloworld as hw
from testfiles import video as v
import led_control as lc
import yeelight_control as yc

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

api.add_resource(hw.HelloWorld, "/helloworld/<string:name>")
api.add_resource(v.Video, "/video/<int:video_id>")

api.add_resource(lc.LED_Control, "/led/<int:led_num>/<string:status>")
api.add_resource(lc.LED_Status, "/led")
api.add_resource(lc.LED_Blink, "/led/<int:led_num>/blink/<float:interval>")

api.add_resource(yc.YeelightPower, "/yeelight/power/<string:status>")
api.add_resource(yc.YeelightBrightness, "/yeelight/brightness/<int:brightness>")
api.add_resource(yc.YeelightColor, "/yeelight/color/<int:r>/<int:g>/<int:b>")
api.add_resource(yc.YeelightStatus, "/yeelight")
api.add_resource(yc.YeelightTemperature, "/yeelight/temperature/<int:temperature>")
api.add_resource(yc.YeelightHueSaturation, "/yeelight/hs/<int:hue>/<int:saturation>")
api.add_resource(yc.ColorDatabase, "/colors")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")