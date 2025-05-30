import requests

CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'

def get_token():
    url = 'https://api.crowdstrike.com/oauth2/token'
    data = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()['access_token']

def get_containment_status(device_id, token):
    url = f"https://api.crowdstrike.com/devices/entities/devices/v1?ids={device_id}"
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    token = get_token()
    device_id = 'device-id'
    status = get_containment_status(device_id, token)
    print(status)
