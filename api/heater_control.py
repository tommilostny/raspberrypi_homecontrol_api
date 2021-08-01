from datetime import datetime
from threading import Thread

from colorama import Fore, Style

from lcd_control import LCD_CELSIUS, display_controller
from multiplug import Multiplug
from temperature import thresholds, log_temperature_event, read_temperature


def control_heater(temperature:float, threshold:float):
    multi_plug = Multiplug()
    power = multi_plug.get_power("heater")
    event_name = None

    if temperature < threshold - 0.1 and power != "on":
        event_name = "heater_low"
        multi_plug.set_power("heater", "on")
        power = "on"
        
    elif temperature > threshold + 0.1 and power != "off":
        event_name = "heater_high"
        multi_plug.set_power("heater", "off")
        power = "off"

    log_temperature_event(event_name, temperature, threshold)
    return power


def control_fan(temperature:float, threshold:float):
    multi_plug = Multiplug()
    power = multi_plug.get_power("fan")
    event_name = None

    if temperature > threshold and power != "on":
        event_name = "fan_high"
        multi_plug.set_power("fan", "on")
        power = "on"

    elif temperature < threshold - 0.1 and power != "off":
        event_name = "fan_low"
        multi_plug.set_power("fan", "off")
        power = "off"

    log_temperature_event(event_name, temperature, threshold)
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
                power_heater = control_heater(temp_c, thresholds.values["day"])
            else: #night
                power_heater = control_heater(temp_c, thresholds.values["night"])

            power_fan = control_fan(temp_c, thresholds.values["fan"])

            if display_controller.is_on():
                display_controller.clear()
                display_controller.print(f"{temp_c}{LCD_CELSIUS}", 1)
                display_controller.print(f"H:{power_heater}, F:{power_fan}", 2)

            event_is_set = self.stop_event.wait(1)
            if event_is_set:
                print(f"{Fore.YELLOW}Stopping heater control...{Style.RESET_ALL}")
                display_controller.turn_off()
                break
