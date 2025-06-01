import os

SEARCH_PATHS = [
    "/Library/LaunchAgents/",
    "/Library/LaunchDaemons/",
    os.path.expanduser("~/Library/LaunchAgents/")
]

def list_plists():
    print("🔍 Scanning for suspicious launch items...\n")
    for path in SEARCH_PATHS:
        if os.path.exists(path):
            for file in os.listdir(path):
                if file.endswith(".plist"):
                    full_path = os.path.join(path, file)
                    print(f"📄 {full_path}")
                    with open(full_path, "r", errors="ignore") as f:
                        content = f.read()
                        if "script" in content or "/tmp/" in content or "curl" in content:
                            print(f"⚠️ Suspicious content in {file}")

if __name__ == "__main__":
    list_plists()
