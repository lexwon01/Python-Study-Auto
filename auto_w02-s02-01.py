import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("MERAKI_API_KEY")


def get_org_id(api_key, org_name):
    url = "https://api.meraki.com/api/v1/organizations"
    headers = {"X-Cisco-Meraki-API-Key": api_key}
    response = requests.get(url, headers=headers)
    orgs = response.json()
    for org in orgs:
        if org["name"] == org_name:
            return org["id"]
    return None


def get_network_id(api_key, org_id, network_name):
    url = f"https://api.meraki.com/api/v1/organizations/{org_id}/networks"
    headers = {"X-Cisco-Meraki-API-Key": api_key}
    response = requests.get(url, headers=headers)
    networks = response.json()
    for network in networks:
        if network["name"] == network_name:
            return network["id"]
    return None


def get_devices(api_key, network_id):
    url = f"https://api.meraki.com/api/v1/networks/{network_id}/devices"
    headers = {"X-Cisco-Meraki-API-Key": api_key}
    response = requests.get(url, headers=headers)
    devices = response.json()
    return devices


def print_devices(devices):
    for device in devices:
        print(f"{device['model']} | {device['serial']} | {device['firmware']}")


org_id = get_org_id(api_key, "RE-SOLUTION LTD")
if org_id is None:
    print("Org not found")
    exit()

network_id = get_network_id(api_key, org_id, "Meraki Lab")
if network_id is None:
    print("Network ID not found")
    exit()

devices = get_devices(api_key, network_id)

print_devices(devices)
