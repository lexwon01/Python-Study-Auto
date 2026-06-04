devices = [
    {"hostname": "R1", "ip": "10.10.10.1", "type": "router", "site": "NY"},
    {"hostname": "SW1", "ip": "10.10.20.1", "type": "switch", "site": "NY"},
    {"hostname": "AP1", "ip": "10.10.30.1", "type": "ap", "site": "NY"},
    {"hostname": "R2", "ip": "10.20.10.1", "type": "router", "site": "Chicago"},
    {"hostname": "SW2", "ip": "10.20.20.1", "type": "switch", "site": "Chicago"},
    {"hostname": "AP2", "ip": "10.20.30.1", "type": "ap", "site": "Chicago"},
    {"hostname": "R3", "ip": "10.30.10.1", "type": "router", "site": "London"},
    {"hostname": "SW3", "ip": "10.30.20.1", "type": "switch", "site": "London"},
    {"hostname": "AP3", "ip": "10.30.30.1", "type": "ap", "site": "London"},
]


def filter_by_field(devices, field, value):
    result = []

    for device in devices:
        if device[field] == value:
            result.append(device)
    return result


devices = filter_by_field(devices, "site", "London")


def print_device(devices):

    for device in devices:
        print(
            f"{device['hostname']} | {device['ip']} | {device['type']} | {device['site']}"
        )


print_device(devices)
