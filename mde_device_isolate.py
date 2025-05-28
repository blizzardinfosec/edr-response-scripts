import requests

TOKEN = 'your-bearer-token'

def isolate_device(device_id):
    url = f'https://api.securitycenter.windows.com/api/machines/{device_id}/isolate'
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        "Comment": "Automated isolation due to detection."
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    device_id = input("Enter device ID to isolate: ")
    result = isolate_device(device_id)
    print("Isolation result:", result)
