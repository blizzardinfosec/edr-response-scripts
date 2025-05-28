import requests

API_TOKEN = 'your-api-token'
SITE_ID = 'your-site-id'

def quarantine_device(device_id):
    url = f"https://your-sentinelone-domain/web/api/v2.1/agents/actions/quarantine"
    headers = {
        'Authorization': f'ApiToken {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        "filter": {
            "siteIds": [SITE_ID],
            "ids": [device_id]
        }
    }
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    device_id = input("Enter device ID to quarantine: ")
    result = quarantine_device(device_id)
    print("Quarantine result:", result)
