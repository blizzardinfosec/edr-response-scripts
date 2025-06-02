import os
import subprocess
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
bundle_dir = f"/tmp/linux_triage_{timestamp}"

def collect():
    os.makedirs(bundle_dir, exist_ok=True)
    print(f"📦 Collecting triage bundle at {bundle_dir}...")

    subprocess.run(f"cp /var/log/auth.log {bundle_dir}/auth.log 2>/dev/null", shell=True)
    subprocess.run(f"cp /var/log/syslog {bundle_dir}/syslog 2>/dev/null", shell=True)
    subprocess.run(f"cp /etc/passwd {bundle_dir}/passwd", shell=True)
    subprocess.run(f"cp /etc/shadow {bundle_dir}/shadow", shell=True)
    subprocess.run(f"ps aux > {bundle_dir}/ps.txt", shell=True)
    subprocess.run(f"netstat -tunap > {bundle_dir}/netstat.txt", shell=True)
    subprocess.run(f"ss -tulwn > {bundle_dir}/sockets.txt", shell=True)

    archive = f"{bundle_dir}.tar.gz"
    subprocess.run(f"tar czf {archive} -C /tmp {os.path.basename(bundle_dir)}", shell=True)
    print(f"✅ Triage archive saved as {archive}")

if __name__ == "__main__":
    collect()
