import requests
from dotenv import load_dotenv
import os
from datetime import datetime

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
        flag = " *** OFFLINE ***" if status["status"] == "offline" else ""
        print(
            f"{status['name']} | {status['model']} | {status.get('firmware', 'Unknown')} | {status['status']} | {status['lastReportedAt']}{flag}"
        )


def write_report(statuses, clients, filename):

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
            flag = " *** OFFLINE ***" if status["status"] == "offline" else ""
            f.write(
                f"{status['name']} | {status['model']} | {status.get('firmware', 'Unknown')} | {status['status']} | {status['lastReportedAt']}{flag}\n"
            )

        f.write("\n")
        f.write("--- Top Clients (24h) ---\n")

        for client in clients:
            f.write(
                f"{client.get('description', client['mac'])} | {client['ip']} | {client['usage']['total'] / (1024 * 1024):.2f} GB\n"
            )


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
        print(
            f"{client.get('description', client['mac'])} | {client['ip']} | {client['usage']['total'] / (1024 * 1024):.2f} GB"
        )


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

# print_statuses(statuses)

# print_offline_devices(statuses)

merge_firmware(devices, statuses)

print_summary(statuses)

write_report(statuses, clients, "meraki_report.txt")

print_top_clients(clients)
