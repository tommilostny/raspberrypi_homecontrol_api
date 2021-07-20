from flask_restful import Resource
from gpiozero import LED, RGBLED
from colorzero import Color

LED1_GPIO_PIN = 18
LED2_GPIO_PIN = 17

RGBLED1_RED_PIN = 19
RGBLED1_GREEN_PIN = 20
RGBLED1_BLUE_PIN = 21

LED_UV_GPIO_PIN = 26

#led1 = LED(LED1_GPIO_PIN)
#led2 = LED(LED2_GPIO_PIN)
#led_uv = LED(LED_UV_GPIO_PIN)
#led_rgb1 = RGBLED(RGBLED1_RED_PIN, RGBLED1_GREEN_PIN, RGBLED1_BLUE_PIN)
#
#ALL_LEDS = [ led1, led2, led_rgb1, led_uv ]
LEDS_ENABLED = [ False, False, False, False ]

class LED_Status(Resource):
    def get(self):
        return [
            {
                "pins": [ LED1_GPIO_PIN ],
                "isActive": False,#led1.is_active,
                "number": 1,
                "isRGB": False,
                "color": None,
                "name": "Red",
                "enabled": LEDS_ENABLED[0]
            },
            {
                "pins": [ LED2_GPIO_PIN ],
                "isActive": False,#led2.is_active,
                "number": 2,
                "isRGB": False,
                "color": None,
                "name": "Green",
                "enabled": LEDS_ENABLED[1]
            },
            {
                "pins": [
                    RGBLED1_RED_PIN,
                    RGBLED1_GREEN_PIN,
                    RGBLED1_BLUE_PIN
                ],
                "isActive": False,#led_rgb1.is_active,
                "number": 3,
                "isRGB": True,
                "color": [ 0.0, 0.0, 0.0 ],#led_rgb1.value,
                "name": "RGB",
                "enabled": LEDS_ENABLED[2]
            },
            {
                "pins": [ LED_UV_GPIO_PIN ],
                "isActive": False,#led_uv.is_active,
                "number": 4,
                "isRGB": False,
                "color": None,
                "name": "UV",
                "enabled": LEDS_ENABLED[3]
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
        if LEDS_ENABLED[led_num - 1]:
            #led_control(ALL_LEDS[led_num - 1], status)
            return "LED " + str(led_num) + " is set to: " + status
        return "LED not enabled"


class LED_Blink(Resource):
    def get(self, led_num, interval):
        if LEDS_ENABLED[led_num - 1]:
            #ALL_LEDS[led_num - 1].blink(interval, interval)
            return "LED " + str(led_num) + " is blinking."
        return "LED not enabled"


class RGB_LED_Color_ByName(Resource):
    def get(self, name):
        if LEDS_ENABLED[2]:
            pass #led_rgb1.color = Color(name)


class RGB_LED_Color_ByRGB(Resource):
    def get(self, r, g, b):
        if LEDS_ENABLED[2]:
            pass #led_rgb1.color = (r / 255.0, g / 255.0, b / 255.0)
