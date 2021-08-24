from busio import I2C
from board import SCL, SDA
from requests import get
from adafruit_neotrellis.neotrellis import NeoTrellis
from time import sleep


class KeyboardController:
    def __init__(self, api_address:str):
        self.api_address = api_address

        #create trellis on the I2C
        self.trellis = NeoTrellis(I2C(SCL, SDA))
        
        for i in range(16):
            #activate rising edge events on all keys
            self.trellis.activate_key(i, NeoTrellis.EDGE_RISING)
            #activate falling edge events on all keys
            self.trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
        #register callbacks
        self.trellis.callbacks[15] = self.__ledstrip_toggle
        self.trellis.callbacks[14] = self.__lamp_toggle
        self.trellis.callbacks[13] = self.__yeelight_toggle
        self.trellis.callbacks[12] = self.__lights_toggle
        self.trellis.callbacks[8] = self.__lights_prev_color
        self.trellis.callbacks[4] = self.__lights_next_color
        self.trellis.callbacks[1] = self.__lcd_toggle
        self.trellis.callbacks[0] = self.__lights_brightness_cycle

    
    def _key_off(self, index):
        self.trellis.pixels[index] = (0, 0, 0)


    def send_command(self, event, entity_name, command, color = None):
        if event.edge == NeoTrellis.EDGE_RISING:
            if color is None:
                color = get(f"{self.api_address}/{entity_name}").json()["color"].values()

            self.trellis.pixels[event.number] = color
            get(f"{self.api_address}/{entity_name}/{command}")

        elif event.edge == NeoTrellis.EDGE_FALLING:
            self._key_off(event.number)


    def __ledstrip_toggle(self, event):
        self.send_command(event, "ledstrip", "toggle")

    def __lamp_toggle(self, event):
        self.send_command(event, "lamp", "toggle")

    def __yeelight_toggle(self, event):
        self.send_command(event, "yeelight", "toggle")

    def __lights_toggle(self, event):
        self.send_command(event, "lights", "toggle", (255, 0, 0))

    def __lights_brightness_cycle(self, event):
        self.send_command(event, "lights", "brightness_cycle/40/100", (69, 69, 69))

    def __lcd_toggle(self, event):
        self.send_command(event, "heater_lcd", "4", (0, 69, 0))


    def send_color_cycle(self, event, direction):
        if event.edge == NeoTrellis.EDGE_RISING:
            color = get(f"{self.api_address}/lights/color_cycle/{direction}").json().values()
            self.trellis.pixels[event.number] = color
        
        elif event.edge == NeoTrellis.EDGE_FALLING:
            sleep(0.4)
            self._key_off(event.number)


    def __lights_next_color(self, event):
        self.send_color_cycle(event, "next")

    def __lights_prev_color(self, event):
        self.send_color_cycle(event, "previous")
