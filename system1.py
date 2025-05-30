import os
import platform
import psutil
import socket
import subprocess
from datetime import datetime

def get_ip_address():
    """Get the system's IP address."""
    try:
        return socket.gethostbyname(socket.gethostname())
    except socket.error:
        return "Unable to fetch IP address"

def get_disk_usage():
    """Get disk usage using df -h."""
    result = subprocess.run(["df", "-h"], capture_output=True, text=True)
    return result.stdout.strip() if result.stdout else "N/A"

def get_fdisk_info():
    """Get partition details using fdisk -l."""
    result = subprocess.run(["fdisk", "-l"], capture_output=True, text=True)
    return result.stdout.strip() if result.stdout else "N/A"

def get_uptime():
    """Get system uptime."""
    result = subprocess.run(["uptime", "-p"], capture_output=True, text=True)
    return result.stdout.strip() if result.stdout else "N/A"

def get_last_reboot():
    """Get last reboot time."""
    result = subprocess.run(["who", "-b"], capture_output=True, text=True)
    return result.stdout.strip().split(" ", 1)[-1] if result.stdout else "N/A"

def get_last_patch():
    """Get last update time (for Debian-based systems)."""
    result = subprocess.run(["ls", "-lt", "/var/log/apt/history.log"], capture_output=True, text=True)
    return result.stdout.strip().split("\n")[0] if result.stdout else "N/A"

def get_recent_apt_history():
    """Get the last 5 lines from /var/log/apt/history.log."""
    try:
        with open("/var/log/apt/history.log", "r") as file:
            lines = file.readlines()
            return "".join(lines[-5:]).strip() if lines else "No recent history available"
    except FileNotFoundError:
        return "History log not found"

def get_script_run_time():
    """Get the current date and time when the script runs."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_system_info():
    """Collect system information."""
    return {
        "Script Run Time": get_script_run_time(),
        "Hostname": platform.node(),
        "IP Address": get_ip_address(),
        "OS": platform.system(),
        "OS Version": platform.version(),
        "CPU Cores": psutil.cpu_count(logical=True),
        "RAM": f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB",
        "Disk Usage": get_disk_usage(),
        "Partition Info": get_fdisk_info(),
        "Uptime": get_uptime(),
        "Last Reboot": get_last_reboot(),
        "Last Patch": get_last_patch(),
        "Recent APT History": get_recent_apt_history(),
    }

def generate_html_report(info):
    """Generate an HTML report with system info."""
    html = """<html><head><title>System Report</title></head><body>
              <h1>Linux System Report</h1>
              <table border='1' cellspacing='2' cellpadding='5'>"""
    
    for key, value in info.items():
        html += f"<tr><td><b>{key}</b></td><td><pre>{str(value).replace('\n', '<br>')}</pre></td></tr>"
    
    html += "</table></body></html>"
    return html

if __name__ == "__main__":
    info = get_system_info()
    report = generate_html_report(info)

    with open("system1.html", "w") as file:
        file.write(report)

    print("System report generated: system1.html")
