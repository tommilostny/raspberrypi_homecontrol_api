import json
from time import sleep

from flask_restful import Resource
from tinytuya import OutletDevice


def multiplug_init():
    with open("data/multiplug.json") as f:
        tuya_data = json.load(f)
    device1 = OutletDevice(tuya_data["device_id"], tuya_data["ip"], tuya_data["local_key"])
    device1.set_version(3.1)
    return device1


HEATER_PLUG = 2
FAN_PLUG = 3

plug_devices = {
    "monitor" : 1,
    "heater" : HEATER_PLUG,
    "fan" : FAN_PLUG,
    "usb" : 7
}

multi_plug = multiplug_init()


def get_tuya_power_status(device, device_id:int=HEATER_PLUG):
    try:
        data = device.status()
        return "on" if data["dps"][str(device_id)] else "off"
    except:
        sleep(0.5)
    return get_tuya_power_status(device, device_id)


class MultiPlugControl(Resource):
    def get(self, device_name:str, power_status:str):
        if device_name in plug_devices.keys():
            if power_status == "toggle":
                power = get_tuya_power_status(multi_plug, plug_devices[device_name])
                power_status = "on" if power == "off" else "off"

            if power_status == "on":
                multi_plug.turn_on(switch=plug_devices[device_name])
            elif power_status == "off":
                multi_plug.turn_off(switch=plug_devices[device_name])
            return { "message" : f"{device_name} turned {power_status}" }, 200
        else:
            return { "message" : f"Invalid request {device_name}/{power_status}" }, 400


class MultiPlugListDevices(Resource):
    def get(self):
        return plug_devices


class MultiPlugStatus(Resource):
    def get(self):
        try:
            return multi_plug.status()
        except:
            sleep(0.1)
            return self.get()
