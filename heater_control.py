from threading import Thread
from colorama import Fore, Style

import temperature as t
import wh_ifttt_control as wi
from drivers import Lcd

CELSIUS = chr(223) + "C  "
TEMPERATURE_THRESHOLD = 23.5

display = Lcd()

class HC_Thread(Thread):
    def __init__(self, stop_event):
        Thread.__init__(self)
        self.stop_event = stop_event

    def run(self):
        print(f"{Fore.YELLOW}Starting heater control...{Style.RESET_ALL}")
        while True:
            temp_c,_,_ = t.read_temp()
            display.lcd_display_string(str(temp_c) + CELSIUS, 1)
            wi.control_heater(temp_c, TEMPERATURE_THRESHOLD)
            wi.print_heater_status(display)

            event_is_set = self.stop_event.wait(2)
            if event_is_set:
                print(f"{Fore.YELLOW}Stopping heater control...{Style.RESET_ALL}")
                display.lcd_clear()
                display.lcd_backlight(0)
                break
