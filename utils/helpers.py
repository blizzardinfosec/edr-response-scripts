import datetime

def timestamp():
    return datetime.datetime.utcnow().isoformat()

def log(msg):
    print(f"[{timestamp()}] {msg}")
