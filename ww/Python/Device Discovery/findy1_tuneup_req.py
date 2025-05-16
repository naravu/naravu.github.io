import subprocess
import re
import sys

def get_ttl(ip: str) -> int:
    """Runs ping command and extracts TTL value."""
    ping_cmd = ["ping", "-n", "1", ip] if sys.platform.startswith("win") else ["ping", "-c", "1", ip]
    try:
        output = subprocess.run(ping_cmd, capture_output=True, text=True, check=True).stdout
        ttl_match = re.search(r"TTL=(\d+)", output, re.IGNORECASE)
        return int(ttl_match.group(1)) if ttl_match else None
    except subprocess.CalledProcessError:
        return None

def detect_os(ttl: int) -> str:
    """Determines OS based on TTL value."""
    if ttl is None:
        return "❌ Host unreachable or ping failed."

    os_map = {
        range(100, 129): "Windows",
        range(50, 65): "Linux",
        range(1, 50): "Network Device"
    }

    for ttl_range, os_name in os_map.items():
        if ttl in ttl_range:
            return f"✅ {os_name} OS detected (TTL: {ttl})"

    return f"❓ Unknown OS (TTL: {ttl})"

if __name__ == "__main__":
    while True:
        ip = input("Enter IP ('q' to quit): ").strip()
        if ip.lower() == 'q':
            print("🔚 Exiting program. 🚀")
            break
        print(detect_os(get_ttl(ip)))
