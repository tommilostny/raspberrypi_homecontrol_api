from flask_restful import Resource

from drivers import Lcd

display = Lcd()

class LcdPrint(Resource):
    def get(self, message, line):
        if len(message) <= 16 and line >= 1 and line <= 2:
            display.lcd_display_string(message, line)
            return "ok"
        else:
            return { "message" : "Wrong input for LCD (message length <= 16 and available lines are 1, 2)" }

class LcdBacklight(Resource):
    def get(self, state):
        if state == 0 or state == 1:
            display.lcd_backlight(state)
            return "ok"
        else:
            return { "message" : str(state) + " is not a valid backlight state." }
