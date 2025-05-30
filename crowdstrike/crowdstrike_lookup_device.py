from utils.auth import get_falcon_token
import requests

def lookup_device_by_hostname(hostname, token):
    url = f"https://api.crowdstrike.com/devices/queries/devices/v1?filter=hostname:'{hostname}'"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    token = get_falcon_token()
    hostname = input("Enter hostname: ")
    result = lookup_device_by_hostname(hostname, token)
    print("Result:", result)
