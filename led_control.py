#### LED test endpoint ####
from flask_restful import Resource
from gpiozero import LED

led1 = LED(18)
led2 = LED(17)

class LED_Control(Resource):
    def get(self, status):
        if status == "off":
            led1.off()
            led2.off()
        elif status == "on":
            led1.on()
            led2.off()
        else:
            led1.toggle()
            led2.toggle()
            status = "toggled"
        return "LEDs are " + status
#### End of LED test endpoint ####