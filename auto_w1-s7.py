devices = [
    {"hostname": "sw1", "type": "switch"},
    {"hostname": "sw2", "type": "switch"},
    {"hostname": "r1", "type": "router"},
    {"hostname": "fw1", "type": "firewall"},
    {"hostname": "sw3", "type": "switch"},
]


def count_by_type(devices):
    counts = {}

    for device in devices:
        dtype = device["type"]

        if dtype in counts:
            counts[dtype] += 1

        else:
            counts[dtype] = 1

    return counts


result = count_by_type(devices)
print(result)
