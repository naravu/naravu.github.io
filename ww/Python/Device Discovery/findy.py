import subprocess
import re
import sys

def get_ttl(ip: str) -> int:
    """Runs ping and extracts TTL value."""
    ping_cmd = ["ping", "-n", "1", ip] if sys.platform.startswith("win") else ["ping", "-c", "1", ip]
    try:
        output = subprocess.run(ping_cmd, capture_output=True, text=True, check=True).stdout
        if ttl_match := re.search(r"TTL=(\d+)", output, re.IGNORECASE):
            return int(ttl_match.group(1))
    except subprocess.CalledProcessError:
        pass
    return None

def detect_os(ttl: int) -> str:
    """Determines OS based on TTL value."""
    if ttl is None:
        return "❌ Unable to determine OS (Host unreachable)"
    os_type = "Windows" if 100 <= ttl <= 128 else "Linux" if 50 <= ttl <= 64 else "Unknown/Network"
    return f"✅ {os_type} OS (TTL: {ttl})"

if __name__ == "__main__":
    while True:
        ip = input("Enter IP ('q' to quit): ").strip()
        if ip.lower() == 'q':
            print("Bye... 🚀")
            break
        print(detect_os(get_ttl(ip)))
