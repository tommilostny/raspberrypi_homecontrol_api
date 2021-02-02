import requests

#File webhooks_key.txt contains only the Webhooks API key on the first line
def load_webhooks_key():
    f = open("webhooks_key.txt", 'r')
    lines = f.readlines()
    f.close()
    return lines[0]

#IFTTT applet 1: IF Webhook (id="temperature_hight") -> Then Smart Life (turn off Tom's heating)
#IFTTT applet 2: IF Webhook (id="temperature_low")   -> Then Smart Life (turn on Tom's heating)
WEBHOOKS_KEY = load_webhooks_key()

power = None

def send_webhooks_event(event):
    requests.post('https://maker.ifttt.com/trigger/{event_name}/with/key/{key}'.format(event_name=event, key=WEBHOOKS_KEY))
    print(event + " event sent")

def print_heater_status(display):
    if power is not None:
        display.lcd_display_string("Heating is " + power + ". ", 2)

def control_heater(temperature, threshold):
    global power

    if temperature < threshold and power != "on":
        send_webhooks_event("temperature_low")
        power = "on"

    elif temperature >= threshold and power != "off":
        send_webhooks_event("temperature_high")
        power = "off"