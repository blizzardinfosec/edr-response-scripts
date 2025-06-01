import os
import subprocess

CHROME_DB = os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/Login Data")

def check_recent_access():
    if not os.path.exists(CHROME_DB):
        print("❌ Chrome Login Data DB not found.")
        return
    print("📦 Checking access time on Chrome login DB...")
    result = subprocess.run(["stat", "-f", "%Sa", CHROME_DB], capture_output=True, text=True)
    print(f"📅 Last access time: {result.stdout.strip()}")

if __name__ == "__main__":
    check_recent_access()
