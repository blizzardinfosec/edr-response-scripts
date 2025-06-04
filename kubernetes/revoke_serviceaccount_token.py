import subprocess
import sys

def revoke_sa(namespace, sa_name):
    print(f"🔒 Revoking tokens for ServiceAccount: {sa_name} in namespace: {namespace}")
    
    # List secrets associated with the SA
    secrets_output = subprocess.check_output([
        "kubectl", "get", "sa", sa_name, "-n", namespace, "-o", "jsonpath={.secrets[*].name}"
    ]).decode().strip().split()

    for secret in secrets_output:
        print(f"🧨 Deleting secret: {secret}")
        subprocess.run(["kubectl", "delete", "secret", secret, "-n", namespace], check=True)

    print("✅ ServiceAccount tokens revoked.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python revoke_serviceaccount_token.py <namespace> <serviceaccount-name>")
        sys.exit(1)
    revoke_sa(sys.argv[1], sys.argv[2])
