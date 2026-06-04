import json

file = "devices.json"


def load_devices_json(file):
    try:
        with open(file) as f:
            result = json.load(f)

        return result
    except FileNotFoundError:
        print(f"Error: {file} not found!")


devices = load_devices_json(file)


def filter_by_field(devices, field, value):

    result = []

    for device in devices:
        if device[field] == value:
            result.append(device)

    return result


def print_devices(devices):

    for device in devices:
        print(
            f"{device['hostname']} | {device['ip']} | {device['type']} | {device['site']}"
        )


if devices:
    switch = filter_by_field(devices, "type", "switch")
    print_devices(switch)
