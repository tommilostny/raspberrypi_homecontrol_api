import json
from time import sleep

from flask_restful import Resource
from tinytuya import BulbDevice, OutletDevice


def tuya_init():
    #file with information about tuya multi plug
    #json format: { "device_id":"", "ip":"", "local_key":"" }
    with open("data/tuya_outlet.json") as f:
        tuya_data = json.load(f)
    device1 = OutletDevice(tuya_data[0]["device_id"], tuya_data[0]["ip"], tuya_data[0]["local_key"])
    device1.set_version(3.1)
    bulb1 = BulbDevice(tuya_data[1]["device_id"], tuya_data[1]["ip"], tuya_data[1]["local_key"])
    bulb1.set_version(3.3)
    return device1, bulb1


HEATER_PLUG = 2
FAN_PLUG = 3

plug_devices = {
    "monitor" : 1,
    "heater" : HEATER_PLUG,
    "fan" : FAN_PLUG,
    "usb" : 7
}
multi_plug, lamp = tuya_init()


def get_power_status(device, device_id:int=HEATER_PLUG):
    try:
        data = device.status()
        return "on" if data["dps"][str(device_id)] else "off"
    except:
        sleep(0.5)
    return get_power_status(device, device_id)


def get_lamp_mode() -> str:
    try:
        data = lamp.status()
        return data["dps"]["2"]
    except:
        sleep(0.5)
        return get_lamp_mode()



class MultiPlugControl(Resource):
    def get(self, device_name:str, power_status:str):
        if device_name in plug_devices.keys():
            if power_status == "toggle":
                power = get_power_status(multi_plug, plug_devices[device_name])
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


class LampStatus(Resource):
    def get(self):
        try:
            return lamp.status()
        except:
            sleep(0.1)
            return self.get()
