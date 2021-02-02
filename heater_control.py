from threading import Thread
from colorama import Fore, Style
from flask_restful import Resource

import temperature as t
import wh_ifttt_control as wi
from drivers import Lcd

CELSIUS = chr(223) + "C  "
TEMPERATURE_THRESHOLD = 23.5

display = Lcd()
backlight_state = 1

class HC_Thread(Thread):
    def __init__(self, stop_event):
        Thread.__init__(self)
        self.stop_event = stop_event

    def run(self):
        global backlight_state
        print(f"{Fore.YELLOW}Starting heater control...{Style.RESET_ALL}")
        while True:
            temp_c,_,_ = t.read_temp()
            wi.control_heater(temp_c, TEMPERATURE_THRESHOLD)

            if backlight_state == 1:
                display.lcd_display_string(str(temp_c) + CELSIUS, 1)
                wi.print_heater_status(display)

            event_is_set = self.stop_event.wait(2)
            if event_is_set:
                print(f"{Fore.YELLOW}Stopping heater control...{Style.RESET_ALL}")
                display.lcd_clear()
                display.lcd_backlight(0)
                break

class LcdControl(Resource):
    def get(self, state):
        global backlight_state
        if state == 0:
            display.lcd_clear()
        if state == 1 or state == 0:
            display.lcd_backlight(state)
            backlight_state = state
        return { "message" : "LCD backlight set to " + str(state) }