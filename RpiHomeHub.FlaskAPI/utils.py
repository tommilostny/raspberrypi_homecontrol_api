from time import sleep


def clamp_value(value:int, low:int, high:int) -> int:
    value = high if value > high else value
    value =  low if value <  low else value
    return value


def clamp_color(red:int, green:int, blue:int):
    red = clamp_value(red, 0, 255)
    green = clamp_value(green, 0, 255)
    blue = clamp_value(blue, 0, 255)
    return red, green, blue


def get_tuya_power_status(device, device_id:int):
    try:
        data = device.status()
        return "on" if data["dps"][str(device_id)] else "off"
    except:
        sleep(0.5)
    return get_tuya_power_status(device, device_id)
