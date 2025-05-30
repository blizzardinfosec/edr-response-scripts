import requests

TOKEN = 'your-bearer-token'
DEVICE_ID = 'device-id'

def initiate_av_scan(device_id, token):
    url = f"https://api.securitycenter.windows.com/api/machines/{device_id}/runAntiVirusScan"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        "comment": "Initiating AV scan via API",
        "scanType": "Full"
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    result = initiate_av_scan(DEVICE_ID, TOKEN)
    print(result)
