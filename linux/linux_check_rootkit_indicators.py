import os
import subprocess

def check_rootkit_signs():
    print("🧪 Checking for known rootkit indicators...\n")

    suspicious_paths = ["/dev/.udev", "/dev/.init", "/dev/shm/.X*", "/lib/.sso", "/tmp/.X*", "/etc/rc.d/init.d/.. "]
    for path in suspicious_paths:
        if os.path.exists(path):
            print(f"⚠️ Suspicious path found: {path}")

    print("\n🔍 Running 'lsmod' for strange kernel modules...\n")
    subprocess.run(["lsmod"])

    print("\n🧪 Comparing md5sums of core binaries...\n")
    for binary in ["/bin/ps", "/usr/bin/top", "/bin/ls", "/usr/bin/netstat"]:
        if os.path.exists(binary):
            subprocess.run(["md5sum", binary])

if __name__ == "__main__":
    check_rootkit_signs()
