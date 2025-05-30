import os
import shutil
from datetime import datetime

ARTIFACT_PATHS = [
    "C:\\Windows\\System32\\winevt\\Logs\\Security.evtx",
    "C:\\Windows\\System32\\winevt\\Logs\\System.evtx",
    "C:\\Users\\%USERNAME%\\AppData\\Local\\Temp",
    "C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Recent",
]

OUTPUT_DIR = f"IR_Artifacts_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def collect_artifacts():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for path in ARTIFACT_PATHS:
        expanded_path = os.path.expandvars(path)
        try:
            if os.path.isdir(expanded_path):
                shutil.copytree(expanded_path, os.path.join(OUTPUT_DIR, os.path.basename(expanded_path)))
            elif os.path.isfile(expanded_path):
                shutil.copy2(expanded_path, OUTPUT_DIR)
        except Exception as e:
            print(f"Error copying {expanded_path}: {e}")

if __name__ == "__main__":
    collect_artifacts()
    print(f"✅ Artifacts collected to {OUTPUT_DIR}")
