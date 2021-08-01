import json
from time import sleep

from flask_restful import Resource
from tinytuya import OutletDevice
from utils import get_tuya_power_status


class Multiplug:
    monitor_plug = 1
    heater_plug = 2
    fan_plug = 3
    usb_plug = 7

    def __init__(self):
        self.plug_devices = {
            "monitor" : self.monitor_plug,
            "heater" : self.heater_plug,
            "fan" : self.fan_plug,
            "usb" : self.usb_plug
        }
        with open("data/multiplug.json") as f:
            tuya_data = json.load(f)
        self.device = OutletDevice(tuya_data["device_id"], tuya_data["ip"], tuya_data["local_key"])
        self.device.set_version(3.1)


    def get_all_status(self):
        try:
            return self.device.status()
        except:
            sleep(0.5)
            return self.get_all_status()

    
    def get_power(self, device_name:str):
        if device_name in self.plug_devices.keys():
            return get_tuya_power_status(self.device, self.plug_devices[device_name])
        else:
            return None


    def set_power(self, device_name:str, power_status:str):
        if device_name in self.plug_devices.keys():            
            if power_status == "toggle":
                power_status = "on" if self.get_power() == "off" else "off"

            if power_status == "on":
                self.device.turn_on(switch=self.plug_devices[device_name])
            elif power_status == "off":
                self.device.turn_off(switch=self.plug_devices[device_name])

            return { "message" : f"{device_name} turned {power_status}" }, 200
        else:
            return { "message" : f"Invalid request {device_name}/{power_status}" }, 400


class MultiPlugControl(Resource):
    def get(self, device_name:str, power_status:str):
        return Multiplug().set_power(device_name, power_status)


class MultiPlugListDevices(Resource):
    def get(self):
        return Multiplug().plug_devices


class MultiPlugStatus(Resource):
    def get(self):
        return Multiplug().get_all_status()
