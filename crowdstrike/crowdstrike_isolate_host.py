import requests

# Replace with your Falcon API credentials
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'

def get_access_token():
    url = 'https://api.crowdstrike.com/oauth2/token'
    data = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()['access_token']

def isolate_host(device_id, token):
    url = f'https://api.crowdstrike.com/devices/entities/devices-actions/v2'
    headers = {'Authorization': f'Bearer {token}'}
    payload = {
        "action_name": "contain",
        "ids": [device_id]
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    device_id = input("Enter device ID to isolate: ")
    token = get_access_token()
    result = isolate_host(device_id, token)
    print("Isolation result:", result)
