# 🛡️ EDR Response Scripts

A collection of practical response automation scripts for blue team operations. These tools interact with EDR APIs (CrowdStrike, SentinelOne, Defender for Endpoint) and Kubernetes/Docker CLIs to perform:

- 🔒 Host and container isolation  
- 📦 Evidence collection  
- 🚨 Remediation actions  
- 🧪 Forensic artifact capture  

---

## 🧰 Tools Required

- Python 3.x  
- `requests` library  
- Valid API tokens for each platform  
- Secure local storage of credentials (e.g., environment variables, `.env`, vault)

---

## 📂 Script Index

| Script                              | Description |
|-------------------------------------|-------------|
| `crowdstrike_isolate_host.py`       | Isolates a device via CrowdStrike Falcon API |
| `crowdstrike_fetch_artifacts.py`    | Pulls forensic data from a compromised host |
| `sentinelone_quarantine.py`         | Quarantines host via SentinelOne API |
| `mde_device_isolate.py`             | Isolates Windows devices via Microsoft Defender API |
| `k8s_quarantine_node.py`            | Cordons and drains a Kubernetes node to isolate it |
| `delete_malicious_pod.py`           | Force deletes a specific Kubernetes pod |
| `revoke_serviceaccount_token.py`    | Deletes secrets tied to a compromised Kubernetes service account |
| `archive_pod_logs.py`               | Dumps logs from a live pod for forensic retention |
| `terminate_container_by_name.py`    | Stops and removes a Docker container by name |
| `docker_container_file_copy.py`     | Extracts files from a live Docker container |

> ✅ All scripts are designed for use in active response or during tabletop exercises. Built for speed, clarity, and action under pressure.

---

## 🧪 Usage Examples

```bash
# Isolate a CrowdStrike host
python crowdstrike_isolate_host.py <hostname>

# Quarantine a SentinelOne device
python sentinelone_quarantine.py <device-id>

# Drain a Kubernetes node
python k8s_quarantine_node.py <node-name>

# Copy suspicious file from Docker container
python docker_container_file_copy.py <container> /tmp/payload /tmp/payload_copy

## 🚧 Work in progress – more platforms and SOAR integration coming soon.
