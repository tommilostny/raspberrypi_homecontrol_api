import Adafruit_DHT
from gpiozero import LED
from time import sleep

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
CELSIUS = u"\N{DEGREE SIGN}C"

badtemp_led = LED(18)
oktemp_led = LED(17)

TEMPERATURE_THRESHOLD = 25

def are_values_real(humidity, temperature):
   return(humidity is not None and temperature is not None and humidity < 100.0)

try:
    while True:
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

        if are_values_real(humidity, temperature):
            print("Humidity: ", humidity, "%")
            print("Temperature: ", temperature, CELSIUS)
            if temperature < TEMPERATURE_THRESHOLD:
                oktemp_led.on()
                badtemp_led.off()
            else:
                oktemp_led.off()
                badtemp_led.on()
        sleep(2)

except KeyboardInterrupt:
    print("Cleaning up!")
