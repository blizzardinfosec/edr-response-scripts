import requests

CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'

def get_falcon_token():
    url = 'https://api.crowdstrike.com/oauth2/token'
    data = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()['access_token']
