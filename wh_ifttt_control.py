import requests

#IFTTT applet 1: IF Webhook (id="temperature_hight") -> Then Smart Life (turn off Tom's heating)
#IFTTT applet 2: IF Webhook (id="temperature_low")   -> Then Smart Life (turn on Tom's heating)
WEBHOOKS_KEY = ""

POWER_STATUS = None

def send_webhooks_event(event):
    requests.post('https://maker.ifttt.com/trigger/{event_name}/with/key/{key}'.format(event_name=event, key=WEBHOOKS_KEY))
    print(event + " event sent")

def print_heater_status(display):
    if POWER_STATUS is not None:
        display.lcd_display_string("Heating is " + POWER_STATUS + ". ", 2)

def control_heater(temperature, threshold):
    global POWER_STATUS

    if temperature < threshold and POWER_STATUS != "on":
        send_webhooks_event("temperature_low")
        POWER_STATUS = "on"

    elif temperature >= threshold and POWER_STATUS != "off":
        send_webhooks_event("temperature_high")
        POWER_STATUS = "off"