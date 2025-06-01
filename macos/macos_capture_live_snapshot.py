import subprocess

def run(cmd):
    print(f"\n🔧 {cmd}")
    output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(output.stdout)

if __name__ == "__main__":
    run("whoami")
    run("uptime")
    run("last -10")
    run("ps aux | head -n 20")
    run("netstat -an | grep ESTABLISHED | head -n 10")
