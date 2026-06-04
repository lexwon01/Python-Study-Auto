import csv

file = "devices.csv"


def read_file(file):
    try:
        result = []

        devices = open(file)
        reader = csv.DictReader(devices)

        for item in reader:
            result.append(item)

        return result

    except FileNotFoundError:
        print(f"Error: {file} does not exist.")


devices = read_file(file)


def filter_by_field(devices, field, value):

    result = []

    for device in devices:
        if device[field] == value:
            result.append(device)

    return result


switch = filter_by_field(devices, "type", "switch")
print(switch)
