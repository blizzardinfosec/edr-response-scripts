def detect_suspicious_users():
    print("🔍 Checking for suspicious user accounts...\n")
    with open("/etc/passwd", "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if len(parts) > 2:
                username, shell, uid = parts[0], parts[-1], parts[2]
                if shell in ("", "/bin/false", "/sbin/nologin"):
                    continue
                if uid == "0" and username != "root":
                    print(f"⚠️ UID 0 detected for non-root user: {username}")
                elif int(uid) > 1000:
                    print(f"👤 Possible created user: {username} (UID {uid})")

if __name__ == "__main__":
    detect_suspicious_users()
