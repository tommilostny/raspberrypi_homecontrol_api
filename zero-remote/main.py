from time import sleep
from keyboard_controller import KeyboardController

keyboard = KeyboardController("http://192.168.1.242:5000")

print("Starting Zero remote control...")

for i in range(16):
    keyboard.trellis.pixels[i] = (0, 100, 0)
    sleep(0.1)

for i in range(16):
    keyboard.trellis.pixels[i] = (0, 0, 0)
    sleep(0.1)

while True:
    try:
        #call the sync function call any triggered callbacks
        keyboard.trellis.sync()
        #the trellis can only be read every 10 millisecons or so
        sleep(.02)
    except KeyboardInterrupt:
        print("Stopping Zero remote control")
        break

