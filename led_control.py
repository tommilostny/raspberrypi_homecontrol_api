#### LED test endpoint ####
from flask_restful import Resource
from gpiozero import LED

LED1_GPIO_PIN = 18
LED2_GPIO_PIN = 17

led1 = LED(LED1_GPIO_PIN)
led2 = LED(LED2_GPIO_PIN)

class LED_Status(Resource):
    def get(self):
        return {
            "led1": {
                "pin": LED1_GPIO_PIN,
                "is_active": led1.is_active,
                "value": led1.value
            },
            "led2": {
                "pin": LED2_GPIO_PIN,
                "is_active": led2.is_active,
                "value": led2.value
            }
        }

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
        return "LED " + str(led_num) + " is set to: " + status

class LED_Blink(Resource):
    def get(self, led_num, interval):
        if led_num == 1:
            led1.blink(interval, interval)
        elif led_num == 2:
            led2.blink(interval, interval)
        return "LED " + str(led_num) + " is blinking."
#### End of LED test endpoint ####