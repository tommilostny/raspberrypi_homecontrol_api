from datetime import datetime
from threading import Thread

from colorama import Fore, Style

from lcd_control import LCD_CELSIUS, display_controller
from temperature import (TEMPERATURE_THRESHOLD_DAY,
                         TEMPERATURE_THRESHOLD_NIGHT,
                         FAN_TEMPERATURE_THRESHOLD,
                         log_temperature_event, read_temperature)
from tuya_devices import HEATER_PLUG, FAN_PLUG, get_power_status, multi_plug


def control_heater(temperature:float, threshold:float):
    power = get_power_status(multi_plug)
    event_name = None

    if temperature < threshold - 0.1 and power != "on":
        event_name = "heater_low"
        multi_plug.turn_on(switch=HEATER_PLUG)
        power = "on"
        
    elif temperature > threshold + 0.1 and power != "off":
        event_name = "heater_high"
        multi_plug.turn_off(switch=HEATER_PLUG)
        power = "off"

    log_temperature_event(event_name, temperature, threshold)
    return power


def control_fan(temperature:float):
    power = get_power_status(multi_plug, FAN_PLUG)
    event_name = None

    if temperature > FAN_TEMPERATURE_THRESHOLD and power != "on":
        event_name = "fan_high"
        multi_plug.turn_on(switch=FAN_PLUG)
        power = "on"

    elif temperature < FAN_TEMPERATURE_THRESHOLD - 0.2 and power != "off":
        event_name = "fan_low"
        multi_plug.turn_off(switch=FAN_PLUG)
        power = "off"

    log_temperature_event(event_name, temperature, FAN_TEMPERATURE_THRESHOLD)
    return power


class HeaterControlThread(Thread):
    def __init__(self, stop_event):
        Thread.__init__(self)
        self.stop_event = stop_event

    def run(self):
        print(f"{Fore.YELLOW}Starting heater control...{Style.RESET_ALL}")
        while True:
            temp_c,_,_ = read_temperature()
            now = datetime.now()

            if now.hour >= 6 and now.hour <= 22: #day
                power_heater = control_heater(temp_c, TEMPERATURE_THRESHOLD_DAY)
            else: #night
                power_heater = control_heater(temp_c, TEMPERATURE_THRESHOLD_NIGHT)

            power_fan = control_fan(temp_c)

            if display_controller.is_on():
                display_controller.clear()
                display_controller.print(f"{temp_c}{LCD_CELSIUS}", 1)
                display_controller.print(f"H:{power_heater}, F:{power_fan}", 2)

            event_is_set = self.stop_event.wait(2)
            if event_is_set:
                print(f"{Fore.YELLOW}Stopping heater control...{Style.RESET_ALL}")
                display_controller.turn_off()
                break

