import requests

CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'

def get_access_token():
    url = 'https://api.crowdstrike.com/oauth2/token'
    data = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()['access_token']

def fetch_artifacts(device_id, token):
    url = f'https://api.crowdstrike.com/real-time-response/entities/artifacts/v1?device_id={device_id}'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    device_id = input("Enter device ID to fetch artifacts: ")
    token = get_access_token()
    artifacts = fetch_artifacts(device_id, token)
    print("Artifacts:", artifacts)
