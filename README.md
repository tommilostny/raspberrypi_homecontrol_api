# Raspberry Pi Home control API

- **RpiHomeHub.FlaskAPI**: API created using **Python Flask**.
- **RpiHomeHub.BlazorWeb**: Web app control hub created using **.NET 5 Blazor PWA**.

## Hardware
- Raspberry Pi 4 Model B (replaced Raspberry Pi Zero WH)
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

To setup the Tuya devices create **multiplug.json** and **lamp.json** files in the *RpiHomeHub.FlaskAPI/data* folder **each** containing following structure:

`{
    "device_id":"",
    "ip":"",
    "local_key":""
}`

### Runs both API and the web app:

1. `cd RpiHomeHub.FlaskAPI`
2. `python3 main.py`
