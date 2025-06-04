import subprocess
import sys

def kill_container(container_name):
    print(f"🛑 Stopping container: {container_name}")
    subprocess.run(["docker", "stop", container_name], check=True)
    subprocess.run(["docker", "rm", container_name], check=True)
    print("✅ Container terminated and removed.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python terminate_container_by_name.py <container-name>")
        sys.exit(1)
    kill_container(sys.argv[1])
