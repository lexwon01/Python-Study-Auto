import csv

file = "devices.csv"


def load_devices(file):
    result = []

    try:
        with open(file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                result.append(row)
    except FileNotFoundError:
        print(f"Error: file '{file}' not found.")

    return result


def filter_by_field(devices, field, value):
    result = []

    for device in devices:
        if device[field] == value:
            result.append(device)
    return result


def print_device(devices):
    for device in devices:
        print(
            f"{device['hostname']} | {device['ip']} | {device['type']} | {device['site']}"
        )


devices = load_devices(file)
switches = filter_by_field(devices, "type", "switch")
firewalls = filter_by_field(devices, "type", "firewall")
print("--- switches ---")
print_device(switches)
print("--- firewalls ---")
print_device(firewalls)
