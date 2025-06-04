import subprocess
import sys
import os
from datetime import datetime

def archive_logs(namespace, pod_name):
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{pod_name}_{timestamp}.log"
    print(f"📦 Archiving logs from pod: {pod_name}")
    
    with open(filename, 'w') as f:
        subprocess.run(["kubectl", "logs", pod_name, "-n", namespace], stdout=f, check=True)
    
    print(f"✅ Logs saved to {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python archive_pod_logs.py <namespace> <pod-name>")
        sys.exit(1)
    archive_logs(sys.argv[1], sys.argv[2])
