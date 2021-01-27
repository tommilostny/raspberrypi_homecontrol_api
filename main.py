#Library imports
from flask import Flask, request
from flask_restful import Api

#Local modules imports
from testfiles import helloworld as hw
from testfiles import video as v
import led_control as lc

app = Flask(__name__)
api = Api(app)

api.add_resource(hw.HelloWorld, "/helloworld/<string:name>")
api.add_resource(v.Video, "/video/<int:video_id>")
api.add_resource(lc.LED_Control, "/led/<string:status>")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")