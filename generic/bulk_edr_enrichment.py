#!/usr/bin/env python3

"""
Bulk EDR Enrichment Script
Queries CrowdStrike, SentinelOne, and MDE for host metadata using a CSV list of hostnames or IPs.
"""

import csv
import os
import requests
import sys

OUTPUT_FILE = "edr_enrichment_output.csv"

# ======== Setup for CrowdStrike ========
def get_crowdstrike_token():
    r = requests.post("https://api.crowdstrike.com/oauth2/token", data={
        "client_id": os.getenv("FALCON_CLIENT_ID"),
        "client_secret": os.getenv("FALCON_CLIENT_SECRET")
    })
    r.raise_for_status()
    return r.json()["access_token"]

def enrich_crowdstrike(hostname, token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get("https://api.crowdstrike.com/devices/queries/devices/v1",
                     headers=headers, params={"hostname": hostname})
    if not r.ok or not r.json().get("resources"):
        return None
    device_id = r.json()["resources"][0]
    r2 = requests.get("https://api.crowdstrike.com/devices/entities/devices/v2",
                      headers=headers, params={"ids": device_id})
    device = r2.json().get("resources", [{}])[0]
    return {
        "source": "CrowdStrike",
        "hostname": device.get("hostname"),
        "ip": device.get("local_ip"),
        "platform": device.get("platform_name"),
        "last_seen": device.get("last_seen"),
        "isolation": device.get("status"),
        "agent_version": device.get("agent_version"),
        "logged_in_user": device.get("logged_in_user", {}).get("username", "")
    }

# ======== Setup for SentinelOne ========
def enrich_sentinelone(hostname):
    headers = {"Authorization": f"ApiToken {os.getenv('SENTINELONE_API_TOKEN')}"}
    url = "https://your-s1-console.sentinelone.net/web/api/v2.1/agents"
    r = requests.get(url, headers=headers, params={"computerName": hostname})
    if not r.ok or not r.json().get("data"):
        return None
    agent = r.json()["data"][0]
    return {
        "source": "SentinelOne",
        "hostname": agent.get("computerName"),
        "ip": agent.get("networkInterfaces", [{}])[0].get("ipAddress"),
        "platform": agent.get("osName"),
        "last_seen": agent.get("lastActiveDate"),
        "isolation": "Isolated" if agent.get("isolated") else "Not Isolated",
        "agent_version": agent.get("agentVersion"),
        "logged_in_user": agent.get("userName")
    }

# ======== Setup for MDE ========
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

def enrich_mde(hostname, token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get("https://api.securitycenter.microsoft.com/api/machines", headers=headers)
    if not r.ok:
        return None
    for machine in r.json().get("value", []):
        if machine.get("computerDnsName", "").lower() == hostname.lower():
            return {
                "source": "MDE",
                "hostname": machine.get("computerDnsName"),
                "ip": machine.get("lastIpAddress"),
                "platform": machine.get("osPlatform"),
                "last_seen": machine.get("lastSeen"),
                "isolation": "Isolated" if machine.get("isolationStatus") == "Isolated" else "Not Isolated",
                "agent_version": machine.get("agentVersion"),
                "logged_in_user": machine.get("loggedOnUsers", [{}])[0].get("accountName", "")
            }
    return None

# ======== Main Function ========
def main(csv_file):
    cs_token = get_crowdstrike_token()
    mde_token = get_mde_token()
    output = []

    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            hostname = row[0].strip()
            print(f"[*] Enriching: {hostname}")

            result = (enrich_crowdstrike(hostname, cs_token)
                      or enrich_sentinelone(hostname)
                      or enrich_mde(hostname, mde_token))

            if result:
                output.append(result)
                print(f"[+] Found: {result['hostname']} ({result['source']})")
            else:
                print(f"[!] No data found for: {hostname}")

    # Write results
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "source", "hostname", "ip", "platform",
            "last_seen", "isolation", "agent_version", "logged_in_user"
        ])
        writer.writeheader()
        for row in output:
            writer.writerow(row)

    print(f"[✓] Enrichment complete — results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bulk_edr_enrichment.py <input_csv>")
        sys.exit(1)

    main(sys.argv[1])
