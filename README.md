# Raspberry Pi 4 Home control

- **api**: API created using **Python Flask**.
- **RpiHomeHub.BlazorWeb**: Web app control hub created using **.NET 5 Blazor PWA**.

## Run both API and the web app:

1. `cd api`
2. `python3.9 main.py`

---

## Hardware
- Raspberry Pi 4 Model B
- Breadboard
- Yeelight color bulb
- WOOX WiFi Smart Multi-plug (Tuya Power Strip)
- 16x2 LCD display with I2C (drivers from [The Raspberry Pi Guy](https://github.com/the-raspberry-pi-guy/lcd))
- Dallas DS18B20 temperature sensor
- LED strip (circuit inspired by [naztronaut/RaspberryPi-RGBW-Control](https://github.com/naztronaut/RaspberryPi-RGBW-Control))

---

## Setup

Installed .NET 5 and ASP.NET Core SDKs/runtime.

Pip3 libraries required: *tinytuya*, *yeelight*, *flask*, *flask_restful*, *flask_cors*, *gpiozero*.

### Lamp and Multiplug setup

To setup the Tuya devices create **multiplug.json** and **lamp.json** files in the *api/data* folder **each** containing following structure:

`{
    "device_id":"",
    "ip":"",
    "local_key":""
}`

### OpenWeather API

1. Register on https://openweathermap.org/.
2. Get the API key.
3. Get your city ID from http://bulk.openweathermap.org/sample/ in *city.list.json.gz* file.
4. Create file **data/weather_api.json** and store the data here in this format:
    - ``{
    "api_key":"",
    "city_id":""
}``.

---

# Raspberry Pi Zero remote control

In folder *zero-remote* there is a project I'm running on **Raspberry Pi Zero WH** with **Adafruit NeoTrellis** keyboard used as a remote control. It sends commands to the above API running on the *Raspberry Pi 4*.
