import json
from datetime import datetime
from threading import Thread

from colorama import Fore, Style
from tinytuya import OutletDevice

from lcd_control import display_controller, LCD_CELSIUS
from temperature import (TEMPERATURE_THRESHOLD_DAY,
                         TEMPERATURE_THRESHOLD_NIGHT,
                         log_temperature_event,
                         read_temperature)

def tuya_init():
    #file with information about tuya multi plug
    #json format: { "device_id":"", "ip":"", "local_key":"" }
    with open("data/tuya_outlet.json") as f:
        tuya_data = json.load(f)
    device = OutletDevice(tuya_data["device_id"], tuya_data["ip"], tuya_data["local_key"])
    device.set_version(3.1)
    return device

HEATER_PLUG = 2
multi_plug = tuya_init()

def get_power_status(outlet:OutletDevice):
    data = outlet.status()
    return "on" if data["dps"]["2"] else "off"

def control_heater(temperature:float, threshold:float):
    power = get_power_status(multi_plug)
    event_name = None

    if temperature < threshold - 0.1 and power != "on":
        event_name = "temperature_low"
        multi_plug.turn_on(switch=HEATER_PLUG)
        
    elif temperature > threshold + 0.1 and power != "off":
        event_name = "temperature_high"
        multi_plug.turn_off(switch=HEATER_PLUG)

    if event_name is not None:
        log_temperature_event(event_name, temperature, threshold)

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
                control_heater(temp_c, TEMPERATURE_THRESHOLD_DAY)
            
            else: #night
                control_heater(temp_c, TEMPERATURE_THRESHOLD_NIGHT)

            if display_controller.is_on():
                display_controller.print(f"{temp_c}{LCD_CELSIUS}", 1)
                display_controller.print(f"Heating is {get_power_status(multi_plug)}. ", 2)

            event_is_set = self.stop_event.wait(2)
            if event_is_set:
                print(f"{Fore.YELLOW}Stopping heater control...{Style.RESET_ALL}")
                display_controller.turn_off()
                break
