import requests
from datetime import datetime
from time import sleep

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
events_send = 0

def send_webhooks_event(event, temp, threshold):
    global events_send
    try:
        requests.post('https://maker.ifttt.com/trigger/{event_name}/with/key/{key}'.format(event_name=event, key=WEBHOOKS_KEY))

        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S): ")

        f = open("data/temp_events.log", "a+")
        f.write(timestampStr + event + " (" + str(temp) + "\N{DEGREE SIGN}C) threshold: " + str(threshold) + "\N{DEGREE SIGN}C\n")
        f.close()
        events_send = events_send + 1
    except Exception:
        events_send = 0
        sleep(0.2)
        send_webhooks_event(event, temp, threshold)

def print_heater_status(display):
    if power is not None:
        display.lcd_display_string("Heating is " + power + ". ", 2)

def control_heater(temperature, threshold):
    global power, events_send

    if (temperature < threshold - 0.1 and power != "on") or (temperature < threshold - 0.4 and events_send < 3):
        send_webhooks_event("temperature_low", temperature, threshold)
        power = "on"
    elif (temperature > threshold + 0.1 and power != "off") or (temperature > threshold + 0.5 and events_send < 3):
        send_webhooks_event("temperature_high", temperature, threshold)
        power = "off"

    #reset events counter if temperature is in norm
    if temperature > threshold - 0.1 and temperature < threshold + 0.1:
        events_send = 0
