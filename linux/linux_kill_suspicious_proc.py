import subprocess

SUSPICIOUS_KEYWORDS = ["python", "nc", "curl", "wget", "bash", "crypto"]

def get_processes():
    return subprocess.check_output(["ps", "aux"]).decode().splitlines()

def kill_matching():
    procs = get_processes()
    for line in procs:
        if any(word in line for word in SUSPICIOUS_KEYWORDS) and "python" not in line.split()[10]:  # exclude this script
            pid = line.split()[1]
            print(f"🔍 Suspicious process detected: {line}")
            try:
                subprocess.run(["kill", "-9", pid])
                print(f"❌ Killed PID: {pid}")
            except Exception as e:
                print(f"Failed to kill {pid}: {e}")

if __name__ == "__main__":
    kill_matching()
