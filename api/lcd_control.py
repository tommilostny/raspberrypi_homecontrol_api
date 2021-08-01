from os.path import exists

from flask_restful import Resource

from drivers import Lcd

LCD_CELSIUS = chr(223) + "C  "

class LcdDisplayController:
    backlight_file = "data/lcd_backlight_state"

    def __init__(self):
        if exists(self.backlight_file):
            with open(self.backlight_file, "r") as file:
                self.backlight_state = int(file.readline())
        else:
            with open(self.backlight_file, "x") as file:
                file.write("1")
            self.backlight_state = 1

        self.display = Lcd()
        self.display.lcd_backlight(self.backlight_state)


    def set_backlight(self, state:int):
        if state == 1 or state == 0:
            self.display.lcd_backlight(state)

            with open(self.backlight_file, "w") as file:
                file.write(str(state))
            self.backlight_state = state


    def print(self, message:str, line:int):
        self.display.lcd_display_string(message, line)


    def turn_off(self):
        self.display.lcd_clear()
        self.set_backlight(0)
    

    def turn_on(self):
        self.display.lcd_clear()
        self.set_backlight(1)


    def toggle(self):
        self.turn_off() if self.is_on() else self.turn_on()


    def is_off(self):
        return self.backlight_state == 0 or self.backlight_state == 2


    def is_on(self):
        return self.backlight_state == 1


    def set_to_message_mode(self):
        if self.backlight_state != 2:
            self.display.lcd_clear()
        self.backlight_state = 2


    def clear(self):
        self.display.lcd_clear()


display_controller = LcdDisplayController()


class LcdControl(Resource):
    def get(self, state):
        if state == 1:
            display_controller.turn_on()
        elif state == 0:
            display_controller.turn_off()
        else:
            display_controller.toggle()

        return { "message" : "LCD backlight set to " + str(state) }


class LcdMessage(Resource):
    def get(self, message, line):
        display_controller.set_to_message_mode()

        if len(message) <= 16 and line >= 1 and line <= 2:
            display_controller.print(message, line)
            return { "message" : "LCD message ok" }
        else:
            return { "message" : "Wrong input for LCD (message length <= 16 and available lines are 1, 2)" }, 400
