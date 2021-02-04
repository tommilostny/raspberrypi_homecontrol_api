#### LED test endpoint ####
from flask_restful import Resource
from gpiozero import LED, RGBLED
from colorzero import Color

LED1_GPIO_PIN = 18
LED2_GPIO_PIN = 17

RGBLED1_RED_PIN = 19
RGBLED1_GREEN_PIN = 20
RGBLED1_BLUE_PIN = 21

led1 = LED(LED1_GPIO_PIN)
led2 = LED(LED2_GPIO_PIN)
led_rgb1 = RGBLED(RGBLED1_RED_PIN, RGBLED1_GREEN_PIN, RGBLED1_BLUE_PIN)

class LED_Status(Resource):
    def get(self):
        return [
            {
                "pins": [ LED1_GPIO_PIN ],
                "isActive": led1.is_active,
                "number": 1,
                "isRGB": False,
                "color": None
            },
            {
                "pins": [ LED2_GPIO_PIN ],
                "isActive": led2.is_active,
                "number": 2,
                "isRGB": False,
                "color": None
            },
            {
                "pins":
                    [
                        RGBLED1_RED_PIN,
                        RGBLED1_GREEN_PIN,
                        RGBLED1_BLUE_PIN
                    ],
                "isActive": led_rgb1.is_active,
                "number": 3,
                "isRGB": True,
                "color": led_rgb1.value
            }
        ]

def led_control(led, status):
    if status == "off":
        led.off()
    elif status == "on":
        led.on()
    else:
        led.toggle()

class LED_Control(Resource):
    def get(self, led_num, status):
        if led_num == 1:
            led_control(led1, status)
        elif led_num == 2:
            led_control(led2, status)
        elif led_num == 3:
            led_control(led_rgb1, status)
        return "LED " + str(led_num) + " is set to: " + status

class LED_Blink(Resource):
    def get(self, led_num, interval):
        if led_num == 1:
            led1.blink(interval, interval)
        elif led_num == 2:
            led2.blink(interval, interval)
        return "LED " + str(led_num) + " is blinking."

class RGB_LED_Color_ByName(Resource):
    def get(self, name):
        led_rgb1.color = Color(name)

class RGB_LED_Color_ByRGB(Resource):
    def get(self, r, g, b):
        led_rgb1.color = (r / 255.0, g / 255.0, b / 255.0)

#### End of LED test endpoint ####
