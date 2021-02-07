from threading import Thread
from colorama import Fore, Style
from flask_restful import Resource
from datetime import datetime
import os

import temperature as t
import wh_ifttt_control as wi
from drivers import Lcd

LOGFILE = "data/temp_events.log"
CELSIUS = chr(223) + "C  "
TEMPERATURE_THRESHOLD_DAY = 23.0
TEMPERATURE_THRESHOLD_NIGHT = 20.5

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
            now = datetime.now()

            if now.hour >= 6 and now.hour <= 22: #day
                wi.control_heater(temp_c, TEMPERATURE_THRESHOLD_DAY)
            
            else: #night
                wi.control_heater(temp_c, TEMPERATURE_THRESHOLD_NIGHT)

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

class Temperature(Resource):
    def get(self):
        c, f, k = t.read_temp()
        return {
            "tempC" : c,
            "tempF" : f,
            "tempK" : k,
            "thresholdDay": TEMPERATURE_THRESHOLD_DAY,
            "thresholdNight": TEMPERATURE_THRESHOLD_NIGHT
        }

class TemperatureLog(Resource):
    def get(self):
        if os.path.exists(LOGFILE):
            f = open(LOGFILE, "r")
            content = f.readlines()
            f.close()
            return content
        else:
            return []

    def delete(self):
        os.system("rm -f " + LOGFILE)
        return { "message": "Temperature log file deleted." }, 200

class TemperatureThreshold(Resource):
    def get(self, period, threshold):
        global TEMPERATURE_THRESHOLD_DAY, TEMPERATURE_THRESHOLD_NIGHT

        if period == "day":
            TEMPERATURE_THRESHOLD_DAY = threshold
        elif period == "night":
            TEMPERATURE_THRESHOLD_NIGHT = threshold