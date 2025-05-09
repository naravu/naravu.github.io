import subprocess
import re
import sys

def get_ttl(ip):
    """Runs ping and extracts TTL value."""
    ping_cmd = ["ping", "-n", "1", ip] if sys.platform.startswith("win") else ["ping", "-c", "1", ip]
    try:
        output = subprocess.check_output(ping_cmd, stderr=subprocess.STDOUT, universal_newlines=True)
        ttl_match = re.search(r"TTL=(\d+)", output, re.IGNORECASE)
        return int(ttl_match.group(1)) if ttl_match else None
    except subprocess.CalledProcessError:
        return None

def detect_os(ttl):
    """Determines OS based on TTL value."""
    if ttl is None:
        return "❌ Unable to determine OS (Host unreachable)"
    return f"✅ {'Windows' if 100 <= ttl <= 128 else 'Linux' if 50 <= ttl <= 64 else 'Unknown/Network'} OS (TTL: {ttl})"

if __name__ == "__main__":
    ip = input("Enter IP address: ").strip()
    print(detect_os(get_ttl(ip)))
