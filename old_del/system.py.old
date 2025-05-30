import os
import platform
import psutil
import socket
import subprocess

def get_ip_address():
    """Get the system's IP address."""
    return socket.gethostbyname(socket.gethostname())

def get_disk_usage():
    """Get disk usage using df -h."""
    result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
    return result.stdout.split("\n")[1] if result.stdout else "N/A"

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
    return result.stdout.split("\n")[0] if result.stdout else "N/A"

def get_system_info():
    """Collect system information."""
    return {
        "Hostname": platform.node(),
        "IP Address": get_ip_address(),
        "OS": platform.system(),
        "OS Version": platform.version(),
        "CPU Cores": psutil.cpu_count(logical=True),
        "RAM": f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB",
        "Disk Usage": get_disk_usage(),
        "Uptime": get_uptime(),
        "Last Reboot": get_last_reboot(),
        "Last Patch": get_last_patch(),
    }

def generate_html_report(info):
    """Generate an HTML report with system info."""
    html = """<html><head><title>System Report</title></head><body>
              <h1>Linux System Report</h1>
              <table border='1' cellspacing='2' cellpadding='5'>"""
    
    for key, value in info.items():
        html += f"<tr><td><b>{key}</b></td><td>{value}</td></tr>"
    
    html += "</table></body></html>"
    return html

if __name__ == "__main__":
    info = get_system_info()
    report = generate_html_report(info)

    with open("system.html", "w") as file:
        file.write(report)

    print("System report generated: system_report.html")
