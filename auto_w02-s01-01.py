import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("MERAKI_API_KEY")
headers = {"X-Cisco-Meraki-API-Key": api_key}
org_id = "669910444571368420"

response = requests.get("https://api.meraki.com/api/v1/organizations", headers=headers)
print(response.status_code)
print(response.json())

response = requests.get(
    "https://api.meraki.com/api/v1/organizations/669910444571368420/networks",
    headers=headers,
)

response = requests.get(
    "https://api.meraki.com/api/v1/networks/L_669910444571383012/devices",
    headers=headers,
)

print(response.status_code)
print(response.json())

devices = response.json()


def print_devices(devices):

    for device in devices:
        print(f"{device['model']} | {device['serial']} | {device['firmware']}")


print_devices(devices)
