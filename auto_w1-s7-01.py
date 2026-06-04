import json
import csv

file = "devices.csv"


def load_devices(file):
    try:
        result = []

        if file.endswith(".json"):
            with open(file) as f:
                result = json.load(f)

        elif file.endswith(".csv"):
            devices = open(file)
            reader = csv.DictReader(devices)

            for item in reader:
                result.append(item)

        else:
            print(f"Error: {file} is unsupported.")

        return result
    except FileNotFoundError:
        print(f"Error: {file} not found!")


devices = load_devices(file)


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


def count_by_field(devices, field):
    counts = {}

    for device in devices:
        dfield = device[field]

        if dfield in counts:
            counts[dfield] += 1

        else:
            counts[dfield] = 1

    return counts


if devices:
    result = count_by_field(devices, "site")
    print(result)
    result = count_by_field(devices, "type")
    print(result)
    switch = filter_by_field(devices, "type", "switch")
    print_devices(switch)
