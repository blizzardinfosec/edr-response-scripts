import subprocess
import sys
import os

def copy_file(container_name, source_path, destination_path):
    print(f"📂 Copying {source_path} from container {container_name} to {destination_path}")
    subprocess.run(["docker", "cp", f"{container_name}:{source_path}", destination_path], check=True)
    print("✅ File copied.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python docker_container_file_copy.py <container-name> <source-path> <destination-path>")
        sys.exit(1)
    copy_file(sys.argv[1], sys.argv[2], sys.argv[3])
