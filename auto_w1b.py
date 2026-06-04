devices = [
    {"hostname": "R1", "ip": "10.0.10.1", "type": "router"},
    {"hostname": "SW1", "ip": "10.0.20.1", "type": "switch"},
    {"hostname": "R1", "ip": "10.0.10.1", "type": "ap"},
]


def filter_by_type(devices, device_type):
    result = []

    for device in devices:
        if device["type"] == device_type:
            result.append(device)
    return result


switch = filter_by_type(devices, "switch")
print(switch)
