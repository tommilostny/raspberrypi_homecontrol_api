import glob
import os
from time import sleep

from flask_restful import Resource

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    while lines[0] is None or lines[0] == "":
        sleep(0.1)
        lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
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
	
class Temperature(Resource):
    def get(self):
        c, f, k = read_temp()
        return { "tempC" : c, "tempF" : f, "tempK" : k }
