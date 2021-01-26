import Adafruit_DHT
from time import sleep

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

CELSIUS = chr(223) + "C"

def are_values_real(humidity, temperature):
   return(humidity is not None and temperature is not None and humidity < 100.0)

try:
    while True:
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

        if are_values_real(humidity, temperature):
            print(humidity)
            print(temperature)
            print('\n')
        sleep(2)

except KeyboardInterrupt:
    print("Cleaning up!")
