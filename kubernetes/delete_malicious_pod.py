import subprocess
import sys

def delete_pod(namespace, pod_name):
    print(f"🔥 Deleting pod: {pod_name} in namespace: {namespace}")
    subprocess.run(["kubectl", "delete", "pod", pod_name, "-n", namespace, "--grace-period=0", "--force"], check=True)
    print("✅ Pod deleted.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python delete_malicious_pod.py <namespace> <pod-name>")
        sys.exit(1)
    delete_pod(sys.argv[1], sys.argv[2])
