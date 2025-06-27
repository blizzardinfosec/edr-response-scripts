#!/usr/bin/env python3

"""
CrowdStrike Memory Dump Script
Triggers a memory dump of a target process on a specified host via RTR.
"""

import requests
import time
import sys
import os

# CrowdStrike API credentials (use secure vault in production)
FALCON_CLIENT_ID = os.getenv("FALCON_CLIENT_ID")
FALCON_CLIENT_SECRET = os.getenv("FALCON_CLIENT_SECRET")

# CrowdStrike API base
BASE_URL = "https://api.crowdstrike.com"

# Get OAuth2 token
def get_token():
    url = f"{BASE_URL}/oauth2/token"
    r = requests.post(url, data={
        "client_id": FALCON_CLIENT_ID,
        "client_secret": FALCON_CLIENT_SECRET
    })
    r.raise_for_status()
    return r.json()["access_token"]

# Trigger RTR session
def start_rtr_session(token, device_id):
    url = f"{BASE_URL}/real-time-response/entities/sessions/v1"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(url, json={"device_id": device_id}, headers=headers)
    r.raise_for_status()
    return r.json()["resources"][0]["session_id"]

# Run procdump command
def run_memory_dump(token, session_id, pid):
    url = f"{BASE_URL}/real-time-response/entities/execute-command/v1"
    headers = {"Authorization": f"Bearer {token}"}
    command = f"procdump -accepteula -ma {pid} C:\\Windows\\Temp\\dump_{pid}.dmp"
    payload = {
        "base_command": "runscript",
        "command_string": f"runscript -CloudFile=procdump -Command=\"{command}\"",
        "session_id": session_id
    }
    r = requests.post(url, json=payload, headers=headers)
    r.raise_for_status()
    return r.json()

# Entry point
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python crowdstrike_memory_dump.py <device_id> <process_id>")
        sys.exit(1)

    device_id = sys.argv[1]
    pid = sys.argv[2]

    token = get_token()
    session_id = start_rtr_session(token, device_id)
    print(f"[+] RTR session started: {session_id}")

    result = run_memory_dump(token, session_id, pid)
    print(f"[+] Memory dump triggered for PID {pid} on device {device_id}")
    print(result)
