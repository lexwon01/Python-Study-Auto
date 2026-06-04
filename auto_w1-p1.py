import csv

filename = "devices.csv"


def load_devices(filename):
    try:
        result = []

        devices = open(filename)
        reader = csv.DictReader(devices)
        for item in reader:
            result.append(item)
        return result

    except FileNotFoundError:
        print(f"Error: {filename} not found")


devices = load_devices(filename)


def filter_by_field(devices, field, value):
    result = []

    for device in devices:
        if device[field] == value:
            result.append(device)
    return result


switch = filter_by_field(devices, "type", "switch")
print(switch)
