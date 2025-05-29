# 🛡️ EDR Response Scripts

A collection of practical response automation scripts for blue team operations. These tools interact with CrowdStrike, SentinelOne, and Defender for Endpoint APIs to perform:

- 🔒 Host isolation
- 📦 Evidence collection
- 🚨 Remediation actions

## 🧰 Tools
- Python 3.x
- Requests / API tokens
- Secure API key storage

## 📂 Scripts

| Script | Description |
|--------|-------------|
| `crowdstrike_isolate_host.py` | Isolates a device via CrowdStrike Falcon API |
| `crowdstrike_fetch_artifacts.py` | Pulls forensic data from a compromised host |
| `sentinelone_quarantine.py` | Quarantines host via SentinelOne API |
| `mde_device_isolate.py` | Isolates Windows devices via Microsoft Defender API |

Work in progress. Built for speed during an incident.

---

## 🧪 Usage Example

```bash
# Isolate a host
python crowdstrike_isolate_host.py

# Lookup a host by name
python crowdstrike_lookup_device.py
