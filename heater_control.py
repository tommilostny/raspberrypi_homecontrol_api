from threading import Thread
from colorama import Fore, Style
from flask_restful import Resource
import os

import temperature as t
import wh_ifttt_control as wi
from drivers import Lcd

CELSIUS = chr(223) + "C  "
TEMPERATURE_THRESHOLD = 23.0

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

def set_lcd_backlight(state):
    global backlight_state
    if state == 0:
        display.lcd_clear()
    if state == 1 or state == 0:
        display.lcd_backlight(state)
        backlight_state = state

class LcdControl(Resource):
    def get(self, state):
        if state == 1 or state == 0:
            set_lcd_backlight(state)

        else: #toggle
            if backlight_state == 0:
                set_lcd_backlight(1)
            else:
                set_lcd_backlight(0)

        return { "message" : "LCD backlight set to " + str(state) }

LOGFILE = "data/temp_events.log"

class TemperatureLogGet(Resource):
    def get(self):
        if os.path.exists(LOGFILE):
            f = open(LOGFILE, "r")
            content = f.readlines()
            f.close()
            return content
        else:
            return []

class TemperatureLogClear(Resource):
    def get(self):
        os.system("rm -f " + LOGFILE)
