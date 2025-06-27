#!/usr/bin/env python3

"""
Generic EDR Host Isolation Script (CrowdStrike, SentinelOne, MDE)
Looks up a device by IP and isolates it via the appropriate EDR platform.
"""

import os
import requests
import sys

def isolate_crowdstrike(ip):
    print(f"[*] Attempting CrowdStrike isolation for {ip}")
    token = get_crowdstrike_token()
    headers = {"Authorization": f"Bearer {token}"}
    # Search by IP
    r = requests.get("https://api.crowdstrike.com/devices/queries/devices/v1", headers=headers, params={"ip": ip})
    if r.status_code != 200 or not r.json().get("resources"):
        return False
    device_id = r.json()["resources"][0]
    # Isolate host
    url = "https://api.crowdstrike.com/policy/containment/v1/contain"
    r = requests.post(url, headers=headers, json={"device_id": device_id})
    if r.status_code == 201:
        print(f"[+] Isolated {ip} via CrowdStrike.")
        return True
    return False

def get_crowdstrike_token():
    r = requests.post("https://api.crowdstrike.com/oauth2/token", data={
        "client_id": os.getenv("FALCON_CLIENT_ID"),
        "client_secret": os.getenv("FALCON_CLIENT_SECRET")
    })
    r.raise_for_status()
    return r.json()["access_token"]

def isolate_sentinelone(ip):
    print(f"[*] Attempting SentinelOne isolation for {ip}")
    headers = {"Authorization": f"ApiToken {os.getenv('SENTINELONE_API_TOKEN')}"}
    url = "https://your-s1-console.sentinelone.net/web/api/v2.1/agents"
    r = requests.get(url, headers=headers, params={"networkInterfaces.ipAddress": ip})
    if r.status_code != 200 or not r.json().get("data"):
        return False
    agent_id = r.json()["data"][0]["id"]
    # Isolate agent
    iso_url = "https://your-s1-console.sentinelone.net/web/api/v2.1/agents/actions/isolate"
    r = requests.post(iso_url, headers=headers, json={"filter": {"ids": [agent_id]}})
    if r.status_code == 202:
        print(f"[+] Isolated {ip} via SentinelOne.")
        return True
    return False

def isolate_mde(ip):
    print(f"[*] Attempting MDE isolation for {ip}")
    token = get_mde_token()
    headers = {"Authorization": f"Bearer {token}"}
    # Search by IP
    url = f"https://api.securitycenter.microsoft.com/api/machines"
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return False
    for machine in r.json().get("value", []):
        if machine.get("lastIpAddress") == ip:
            machine_id = machine["id"]
            iso_url = f"https://api.securitycenter.microsoft.com/api/machines/{machine_id}/isolate"
            r2 = requests.post(iso_url, headers=headers)
            if r2.status_code == 200:
                print(f"[+] Isolated {ip} via MDE.")
                return True
    return False

def get_mde_token():
    url = f"https://login.microsoftonline.com/{os.getenv('MDE_TENANT_ID')}/oauth2/v2.0/token"
    data = {
        "client_id": os.getenv("MDE_CLIENT_ID"),
        "client_secret": os.getenv("MDE_CLIENT_SECRET"),
        "grant_type": "client_credentials",
        "scope": "https://api.securitycenter.microsoft.com/.default"
    }
    r = requests.post(url, data=data)
    r.raise_for_status()
    return r.json()["access_token"]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generic_isolate_host_by_ip.py <IP_ADDRESS>")
        sys.exit(1)

    ip_address = sys.argv[1]
    if not (isolate_crowdstrike(ip_address) or isolate_sentinelone(ip_address) or isolate_mde(ip_address)):
        print(f"[!] Could not isolate {ip_address} — host not found in EDR platforms.")
