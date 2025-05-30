import requests

API_TOKEN = 'your-api-token'
THREAT_ID = 'threat-id'

def get_threat_details(threat_id):
    url = f"https://your-sentinelone-api.com/web/api/v2.1/threats/{threat_id}"
    headers = {
        'Authorization': f'ApiToken {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    details = get_threat_details(THREAT_ID)
    print(details)
