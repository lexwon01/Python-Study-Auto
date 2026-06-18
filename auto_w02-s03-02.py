import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("MERAKI_API_KEY")


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


org_id = get_org_id(api_key, "RE-SOLUTION LTD")
if org_id is None:
    print("Org not found")
    exit()

network_id = get_network_id(api_key, org_id, "Meraki Lab")
if network_id is None:
    print("Network ID not found")
    exit()

devices = get_devices(api_key, network_id)
if devices is None:
    print("Devices not found")
    exit()

print_devices(devices)

statuses = get_device_statuses(api_key, org_id)
if statuses is None:
    print("Status not found")
    exit()

print_statuses(statuses)

print_offline_devices(statuses)
