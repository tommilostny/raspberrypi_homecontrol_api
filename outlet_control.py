import json
from datetime import datetime
from time import sleep
from tinytuya import OutletDevice


def tuya_init():
    with open("data/tuya_outlet.json") as f:
        tuya_data = json.load(f)
    device = OutletDevice(tuya_data["device_id"], tuya_data["ip"], tuya_data["local_key"])
    device.set_version(3.1)
    return device

def get_power_status(outlet:OutletDevice):
    data = outlet.status()
    return "on" if data["dps"]["2"] else "off"

multi_plug = tuya_init()
power = get_power_status(multi_plug)

HEATER_PLUG = 2

def send_heater_event(event, temp, threshold):
    try:
        if event == "temperature_low":
            multi_plug.turn_on(switch=HEATER_PLUG)
        elif event == "temperature_high":
            multi_plug.turn_off(switch=HEATER_PLUG)

        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S): ")

        with open("data/temp_events.log", "a+") as f:
            f.write(timestampStr + event + " (" + str(temp) + "\N{DEGREE SIGN}C) threshold: " + str(threshold) + "\N{DEGREE SIGN}C\n")
    except Exception:
        sleep(0.2)
        send_heater_event(event, temp, threshold)

def print_heater_status(display):
    if power is not None:
        display.lcd_display_string("Heating is " + power + ". ", 2)

def control_heater(temperature, threshold):
    global power

    if temperature < threshold - 0.1 and power != "on":
        send_heater_event("temperature_low", temperature, threshold)
    elif temperature > threshold + 0.1 and power != "off":
        send_heater_event("temperature_high", temperature, threshold)
    
    power = get_power_status(multi_plug)
