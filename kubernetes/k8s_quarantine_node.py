import subprocess
import sys

def quarantine_node(node_name):
    print(f"🚧 Quarantining node: {node_name}")
    subprocess.run(["kubectl", "cordon", node_name], check=True)
    subprocess.run(["kubectl", "drain", node_name, "--ignore-daemonsets", "--delete-emptydir-data", "--force"], check=True)
    print(f"✅ Node {node_name} quarantined.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python k8s_quarantine_node.py <node-name>")
        sys.exit(1)
    quarantine_node(sys.argv[1])
