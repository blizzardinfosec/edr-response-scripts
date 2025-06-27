#!/usr/bin/env python3

"""
Microsoft Defender for Endpoint - IOC Block Script
Creates a custom indicator to block a file hash, IP, or domain.
"""

import requests
import sys
import os
import json

TENANT_ID = os.getenv("MDE_TENANT_ID")
CLIENT_ID = os.getenv("MDE_CLIENT_ID")
CLIENT_SECRET = os.getenv("MDE_CLIENT_SECRET")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
RESOURCE = "https://api.securitycenter.microsoft.com"
SCOPE = f"{RESOURCE}/.default"
INDICATOR_URL = f"{RESOURCE}/api/indicators"

def get_access_token():
    url = f"{AUTHORITY}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": SCOPE
    }
    r = requests.post(url, data=data)
    r.raise_for_status()
    return r.json()["access_token"]

def create_indicator(token, indicator_type, value, description="Blocked via script"):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "indicatorType": indicator_type,
        "indicatorValue": value,
        "action": "Block",
        "severity": "High",
        "title": f"Block {value}",
        "description": description,
        "recommendedActions": ["Investigate and contain"],
        "expirationTime": None
    }

    r = requests.post(INDICATOR_URL, headers=headers, json=payload)
    r.raise_for_status()
    print(f"[+] Indicator successfully created: {value}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python mde_custom_indicator_block.py <type> <value>")
        print("Type must be one of: FileSha256, IpAddress, Url, DomainName")
        sys.exit(1)

    indicator_type = sys.argv[1]
    value = sys.argv[2]

    token = get_access_token()
    create_indicator(token, indicator_type, value)
