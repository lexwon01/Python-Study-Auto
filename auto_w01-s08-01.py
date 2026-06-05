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
            with open(file) as f:
                reader = csv.DictReader(f)
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


def print_summary(devices):
    print("=== Device Summary ===")

    counts = count_by_field(devices, "type")
    print("By type:")
    for type, count in counts.items():
        print(f" {type} : {count}")

    counts = count_by_field(devices, "site")
    print("By site:")
    for site, count in counts.items():
        print(f" {site} : {count}")


if devices:
    print_summary(devices)
    print("\n=== Full Inventory ===")
    print_devices(devices)
