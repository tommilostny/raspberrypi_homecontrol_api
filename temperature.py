import glob
import os
from datetime import datetime
from time import sleep

from flask_restful import Resource

LOGFILE = "data/temp_events.log"
LOG_CELSIUS = "\N{DEGREE SIGN}C"
TEMPERATURE_THRESHOLD_DAY = 22.3
TEMPERATURE_THRESHOLD_NIGHT = 20.5

FAN_TEMPERATURE_THRESHOLD = 27.5

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


#Returns temperature value from the Dallas DS18B20 sensor in Celsius, Fahrenheit and Kelvin
def read_temperature():
    ok = False
    while not ok:
        try:
            ok = True
            lines = read_temp_raw()
            while lines[0].strip()[-3:] != 'YES':
                sleep(0.2)
                lines = read_temp_raw()
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                temp_f = temp_c * 1.8 + 32.0
                temp_k = temp_c + 273.15
                return temp_c, temp_f, temp_k
            else:
                ok = False
        except IndexError:
            ok = False
            sleep(0.1)


def log_temperature_event(event_name:str, temperature:float, threshold:float):
    if event_name is not None:
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S):")
        with open(LOGFILE, "a+") as f:
            f.write(f"{timestampStr} {event_name} ({temperature}{LOG_CELSIUS}) threshold: {threshold}{LOG_CELSIUS}\n")


class Temperature(Resource):
    def get(self):
        c, f, k = read_temperature()
        return {
            "tempC" : c,
            "tempF" : f,
            "tempK" : k,
            "thresholdDay": TEMPERATURE_THRESHOLD_DAY,
            "thresholdNight": TEMPERATURE_THRESHOLD_NIGHT,
            "fanThreshold": FAN_TEMPERATURE_THRESHOLD
        }


class TemperatureLog(Resource):
    def get(self):
        if os.path.exists(LOGFILE):
            with open(LOGFILE, "r") as f:
                content = f.readlines()
            return content
        else:
            return []

    def delete(self):
        os.system("rm -f " + LOGFILE)
        return { "message": "Temperature log file deleted." }, 200


class TemperatureThreshold(Resource):
    def get(self, period, threshold):
        global TEMPERATURE_THRESHOLD_DAY, TEMPERATURE_THRESHOLD_NIGHT, FAN_TEMPERATURE_THRESHOLD

        if period == "day":
            TEMPERATURE_THRESHOLD_DAY = threshold
        elif period == "night":
            TEMPERATURE_THRESHOLD_NIGHT = threshold
        elif period == "fan":
            FAN_TEMPERATURE_THRESHOLD = threshold

