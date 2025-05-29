import json
import requests
from unittest.mock import patch

@patch('requests.get')
def test_lookup_device(mock_get):
    from crowdstrike_lookup_device import lookup_device_by_hostname

    with open('test/mock_data.json') as f:
        mock_get.return_value.json.return_value = json.load(f)
        mock_get.return_value.status_code = 200

    token = "mock-token"
    hostname = "test-machine"
    result = lookup_device_by_hostname(hostname, token)

    assert "resources" in result
    print("✅ Test passed.")
