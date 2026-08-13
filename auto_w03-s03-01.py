import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import csv
from jinja2 import Environment, FileSystemLoader
import yaml

load_dotenv()

api_key = os.getenv("MERAKI_API_KEY")
org_id = os.getenv("ORG_ID")
net_id = os.getenv("NET_ID")


def get_org_id(api_key, org_name):
    url = "https://api.meraki.com/api/v1/organizations"
    headers = {"X-Cisco-Meraki-API-Key": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"API error: {response.status_code}")
        return None
    orgs = response.json()
    for org in orgs:
        if org["name"] == org_name:
            return org["id"]
    return None


def get_network_id(api_key, org_id, network_name):
    url = f"https://api.meraki.com/api/v1/organizations/{org_id}/networks"
    headers = {"X-Cisco-Meraki-API-Key": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"API error: {response.status_code}")
        return None
    networks = response.json()
    for network in networks:
        if network["name"] == network_name:
            return network["id"]
    return None


def get_devices(api_key, network_id):
    url = f"https://api.meraki.com/api/v1/networks/{network_id}/devices"
    headers = {"X-Cisco-Meraki-API-Key": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"API error: {response.status_code}")
        return None
    devices = response.json()
    return devices


def print_devices(devices):
    for device in devices:
        print(f"{device['model']} | {device['serial']} | {device['firmware']}")


def get_org_devices(api_key, org_id):
    url = f"https://api.meraki.com/api/v1/organizations/{org_id}/devices"
    headers = {"X-Cisco-Meraki-API-Key": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"API error: {response.status_code}")
        return None
    org_devices = response.json()
    return org_devices


def get_device_statuses(api_key, org_id):
    url = f"https://api.meraki.com/api/v1/organizations/{org_id}/devices/statuses"
    headers = {"X-Cisco-Meraki-API-Key": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"API error: {response.status_code}")
        return None
    statuses = response.json()
    return statuses


def print_statuses(statuses):
    for status in statuses:
        print(
            f"{status['name']} | {status['model']} | {status['status']} | {status['lastReportedAt']}"
        )


def print_offline_devices(statuses):
    for status in statuses:
        if status["status"] != "online":
            print(f"Device {status['name']} is OFFLINE")


def print_summary(statuses):
    total_count = 0
    offline_count = 0

    for status in statuses:
        total_count += 1

        if status["status"] == "offline":
            offline_count += 1
    print("=== Meraki Health Report ===")
    print(f"Total devices: {total_count}")
    print(f"Offline: {offline_count}")
    print()
    print("--- Device Status ---")

    for status in statuses:
        print(format_device_line(status))


def write_report(statuses, clients, vpns, filename):

    dt = datetime.now()

    total_count = 0
    offline_count = 0

    for status in statuses:
        total_count += 1

        if status["status"] == "offline":
            offline_count += 1

    with open(filename, "w") as f:
        f.write("=== Meraki Health Report ===\n")
        f.write(dt.strftime("%Y-%m-%d %H:%M\n"))
        f.write(f"Total devices: {total_count}\n")
        f.write(f"Offline: {offline_count}\n")
        f.write("\n")
        f.write("--- Device Status ---\n")

        for status in statuses:
            f.write(format_device_line(status) + "\n")

        f.write("\n")
        f.write("--- Top Clients (24h) ---\n")

        for client in clients:
            f.write(format_client_line(client) + "\n")

        f.write("--- VPN Status ---\n")
        if vpns is None:
            f.write("VPN status: unavailable\n")
        else:
            for hub in vpns["hubs"]:
                f.write(format_vpn_hub_line(hub) + "\n")

            for subnet in vpns["subnets"]:
                f.write(format_vpn_subnet_line(subnet) + "\n")

        f.write("\n")
        f.write("--- Dormant Devices ---\n")
        for status in statuses:
            if status["status"] == "dormant":
                f.write(format_dormant_line(status) + "\n")


def merge_firmware(devices, statuses):
    for status in statuses:
        for device in devices:
            if status["serial"] == device["serial"]:
                status["firmware"] = device.get("firmware", "Unknown")
    return statuses


def get_top_clients(api_key, network_id):
    url = f"https://api.meraki.com/api/v1/networks/{network_id}/clients?perPage=5&timespan=86400"
    headers = {"X-Cisco-Meraki-API-Key": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"API error: {response.status_code}")
        return None
    clients = response.json()
    return clients


def print_top_clients(clients):
    print()
    print("--- Top Clients (24h) ---")
    for client in clients:
        print(format_client_line(client))


def get_vpn_statuses(api_key, network_id):
    url = f"https://api.meraki.com/api/v1/networks/{network_id}/appliance/vpn/siteToSiteVpn"
    headers = {"X-Cisco-Meraki-API-Key": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"API error: {response.status_code}")
        return None
    vpns = response.json()
    return vpns


def load_devices_yaml(file):
    try:
        if file.endswith(".yaml"):
            with open(file) as f:
                devices = yaml.safe_load(f)
            return devices
    except FileNotFoundError:
        print(f"Error: {file} not found!")


def filter_by_field(devices, field, value):

    result = []

    for device in devices:
        if device[field] == value:
            result.append(device)

    return result


def count_by_field(devices, field):
    counts = {}

    for device in devices:
        dfield = device[field]

        if dfield in counts:
            counts[dfield] += 1

        else:
            counts[dfield] = 1

    return counts


def print_vpn_statuses(vpns):
    # print(f"{vpns['mode']} | {vpns['hubs']} | {vpns['subnets']}")
    print()
    print("--- Site-to-Site VPN Details ---")

    for hub in vpns["hubs"]:
        print(format_vpn_hub_line(hub))

    for subnet in vpns["subnets"]:
        print(format_vpn_subnet_line(subnet))


def print_dormant_devices(statuses):
    print()
    for status in statuses:
        if status["status"] == "dormant":
            print(format_dormant_line(status))


def write_report_csv(statuses, filename):
    with open(filename, "w", newline="") as f:
        fieldnames = ["name", "model", "status", "firmware", "lastReportedAt"]
        writer = csv.DictWriter(
            f, fieldnames=fieldnames, restval="Unknown", extrasaction="ignore"
        )
        writer.writeheader()
        for status in statuses:
            row = {**status, "name": status.get("name") or status.get("model")}
            writer.writerow(row)


def format_device_line(status):
    flag = " *** OFFLINE ***" if status["status"] == "offline" else ""
    return f"{status.get('name') or status.get('model')} | {status.get('firmware', 'Unknown')} | {status['status']} | {status['lastReportedAt']}{flag}"


def format_client_line(client):
    return f"{client.get('description', client['mac'])} | {client['ip']} | {client['usage']['total'] / (1024 * 1024):.2f} GB"


def format_vpn_hub_line(hub):
    return f"Hub ID: {hub['hubId']}"


def format_vpn_subnet_line(subnet):
    return f"Local subnet: {subnet['localSubnet']} | In use: {subnet['useVpn']}"


def format_dormant_line(status):
    return f"Device {status.get('name') or status.get('model')} is DORMANT"


org_id = get_org_id(api_key, org_id)
if org_id is None:
    print("Org not found")
    exit()

network_id = get_network_id(api_key, org_id, net_id)
if network_id is None:
    print("Network ID not found")
    exit()

devices = get_devices(api_key, network_id)
if devices is None:
    print("Devices not found")
    exit()

# print_devices(devices)

statuses = get_device_statuses(api_key, org_id)
if statuses is None:
    print("Status not found")
    exit()

clients = get_top_clients(api_key, network_id)
if clients is None:
    print("Clients not found")
    exit()

vpns = get_vpn_statuses(api_key, network_id)
if vpns is None:
    print("VPN status: unavailable")
    exit()
org_devices = get_org_devices(api_key, org_id)
if org_devices is None:
    print("Org devices not found")
    exit()


# print_statuses(statuses)

# print_offline_devices(statuses)

merge_firmware(org_devices, statuses)

env = Environment(loader=FileSystemLoader("."))
template = env.get_template("report_template.html")
html = template.render(statuses=statuses, vpns=vpns)


def write_report_html(html, filename):
    with open(filename, "w", newline="") as f:
        f.write(html)


def load_interfaces_yaml(file):
    try:
        if file.endswith(".yaml"):
            with open(file) as f:
                interfaces = yaml.safe_load(f)
            return interfaces
    except FileNotFoundError:
        print(f"Error: {file} not found!")


print_summary(statuses)

write_report(statuses, clients, vpns, "meraki_report.txt")

write_report_csv(statuses, "meraki_report.csv")

write_report_html(html, "meraki_report.html")

print_top_clients(clients)

print_vpn_statuses(vpns)

print_dormant_devices(statuses)

yaml_devices = load_devices_yaml("devices.yaml")
print(yaml_devices)


yaml_interfaces = load_interfaces_yaml("interfaces.yaml")
if yaml_interfaces is None:
    print("Interfaces not found")
    exit()
first_interface = yaml_interfaces[0]

for yaml_interface in yaml_interfaces:
    template = env.get_template("interface_template.j2")
    rendered = template.render(
        hostname=yaml_interface["hostname"],
        interface=yaml_interface["interface"],
        description=yaml_interface.get("description", ""),
    )
    print(rendered)


grouped = {}

for yaml_interface in yaml_interfaces:
    hostname = yaml_interface["hostname"]

    if hostname not in grouped:
        grouped[hostname] = []

    grouped[hostname].append(yaml_interface)

#print(grouped)
    

for hostname, interfaces in grouped.items():
    with open(f"{hostname}.txt", "w") as f:
        for iface in interfaces:
            rendered = template.render(
                hostname=iface["hostname"],
                interface=iface["interface"],
                description=iface.get("description", ""),
            )
            f.write(rendered + "\n")



filter_devices = filter_by_field(yaml_devices, "site", "Branch1")
#print(filter_devices)

count_devices = count_by_field(yaml_devices, "type")
#print(count_devices)
