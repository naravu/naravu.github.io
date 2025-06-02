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
    """Get disk usage using PowerShell's Get-PSDrive."""
    result = subprocess.run(["powershell", "-Command", "Get-PSDrive | Where-Object {$_.Used -ne $null} | Format-Table -AutoSize"], capture_output=True, text=True)
    return result.stdout.strip() if result.stdout else "N/A"

def get_partition_info():
    """Get partition details using PowerShell's Get-Partition."""
    result = subprocess.run(["powershell", "-Command", "Get-Partition | Format-Table -AutoSize"], capture_output=True, text=True)
    return result.stdout.strip() if result.stdout else "N/A"

def get_uptime():
    """Get system uptime using PowerShell."""
    result = subprocess.run(["powershell", "-Command", "(Get-CimInstance Win32_OperatingSystem).LastBootUpTime"], capture_output=True, text=True)
    return result.stdout.strip() if result.stdout else "N/A"

def get_last_reboot():
    """Get last reboot time using PowerShell."""
    result = subprocess.run(["powershell", "-Command", "systeminfo | find \"System Boot Time\""], capture_output=True, text=True)
    return result.stdout.strip() if result.stdout else "N/A"

def get_installed_updates():
    """Get last installed updates using PowerShell."""
    result = subprocess.run(["powershell", "-Command", "Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 5"], capture_output=True, text=True)
    return result.stdout.strip() if result.stdout else "N/A"

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
        "Partition Info": get_partition_info(),
        "Uptime": get_uptime(),
        "Last Reboot": get_last_reboot(),
        "Installed Updates": get_installed_updates(),
    }

def generate_html_report(info):
    """Generate an HTML report with system info."""
    html = """<html><head><title>Windows System Report</title></head><body>
              <table border='1' cellspacing='2' cellpadding='5'>"""
    
    for key, value in info.items():
        html += f"<tr><td><b>{key}</b></td><td><pre>{str(value).replace('\n', '<br>')}</pre></td></tr>"
    
    html += "</table></body></html>"
    return html

if __name__ == "__main__":
    info = get_system_info()
    report = generate_html_report(info)

    with open("winsystem.html", "w") as file:
        file.write(report)

    print("System report generated: winsystem.html")
