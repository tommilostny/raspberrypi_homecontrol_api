import time
from board import SCL, SDA
import busio
from adafruit_neotrellis.neotrellis import NeoTrellis
import requests

#create the i2c object for the trellis
i2c_bus = busio.I2C(SCL, SDA)

#create the trellis
trellis = NeoTrellis(i2c_bus)


def toggle_led_strip(event):
    if event.edge == NeoTrellis.EDGE_RISING:
        color = requests.get("http://192.168.1.242:5000/ledstrip").json()["color"].values()
        trellis.pixels[event.number] = color
        requests.get("http://192.168.1.242:5000/ledstrip/toggle")

    elif event.edge == NeoTrellis.EDGE_FALLING:
        trellis.pixels[event.number] = (0, 0, 0)


print("Starting Zero remote control...")

for i in range(16):
    #activate rising edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_RISING)
    #activate falling edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_FALLING)

    trellis.pixels[i] = (0, 255, 0)
    time.sleep(0.1)

trellis.callbacks[0] = toggle_led_strip

for i in range(16):
    trellis.pixels[i] = (0, 0, 0)
    time.sleep(0.1)

while True:
    try:
        #call the sync function call any triggered callbacks
        trellis.sync()
        #the trellis can only be read every 10 millisecons or so
        time.sleep(.02)
    except KeyboardInterrupt:
        print("Stopping Zero remote control")
        break

