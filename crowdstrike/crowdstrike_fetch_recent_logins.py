import requests

CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"

def get_token():
    r = requests.post("https://api.crowdstrike.com/oauth2/token", data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })
    r.raise_for_status()
    return r.json()["access_token"]

def fetch_recent_logins(device_id, token):
    url = f"https://api.crowdstrike.com/incidents/queries/incidents/v1?filter=device_id:'{device_id}'"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    print("Login-related incidents:")
    for i in r.json().get("resources", []):
        print(f"  • {i}")

if __name__ == "__main__":
    device_id = input("Enter device ID: ")
    token = get_token()
    fetch_recent_logins(device_id, token)
