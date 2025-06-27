#!/usr/bin/env python3

"""
SentinelOne Network Quarantine Script
Restricts outbound network access on a host without full isolation.
"""

import requests
import sys
import os

S1_API_TOKEN = os.getenv("SENTINELONE_API_TOKEN")  # Use environment variable
S1_CONSOLE_URL = "https://your-s1-console.sentinelone.net"  # Update as needed

HEADERS = {
    "Authorization": f"ApiToken {S1_API_TOKEN}",
    "Content-Type": "application/json"
}

def get_agent_id(hostname):
    url = f"{S1_CONSOLE_URL}/web/api/v2.1/agents"
    params = {"computerName": hostname}
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    agents = r.json().get("data", [])
    if not agents:
        raise Exception(f"No agents found for hostname: {hostname}")
    return agents[0]["id"]

def restrict_network(agent_id):
    url = f"{S1_CONSOLE_URL}/web/api/v2.1/agents/actions/restrict-network"
    data = {"filter": {"ids": [agent_id]}}
    r = requests.post(url, headers=HEADERS, json=data)
    r.raise_for_status()
    print(f"[+] Network restriction command sent to agent: {agent_id}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sentinelone_network_quarantine.py <hostname>")
        sys.exit(1)

    hostname = sys.argv[1]
    try:
        agent_id = get_agent_id(hostname)
        restrict_network(agent_id)
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)
