from threading import Thread
from time import sleep

import temperature as t
from drivers import Lcd

CELSIUS = chr(223) + "C  "
TEMPERATURE_THRESHOLD = 23.5

display = Lcd()
is_heating_on = None

def print_heating_status(temp):
    if temp < TEMPERATURE_THRESHOLD:
        display.lcd_display_string("Heating is on.", 2)
    else:
        display.lcd_display_string("Heating is off.", 2)

class HC_Thread(Thread):
    def __init__(self, stop_event):
        Thread.__init__(self)
        self.stop_event = stop_event

    def run(self):
        print("Starting heater control...")
        while True:
            temp_c,_,_ = t.read_temp()
            display.lcd_display_string(str(temp_c) + CELSIUS, 1)
            print_heating_status(temp_c)

            event_is_set = self.stop_event.wait(1)
            if event_is_set:
                print("Stopping heater control...")
                display.lcd_clear()
                display.lcd_backlight(0)
                break