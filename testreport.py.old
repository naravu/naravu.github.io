import os
import platform
import psutil

def get_system_info():
    return {
        "Hostname": platform.node(),
        "OS": platform.system(),
        "OS Version": platform.version(),
        "CPU Cores": psutil.cpu_count(logical=True),
        "RAM": f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB",
        "Disk Usage": f"{psutil.disk_usage('/').percent}%",
    }

def generate_html_report(info):
    html = "<html><head><title>System Report</title></head><body>"
    html += "<h1>Linux System Report</h1><table border='0'>"
    for key, value in info.items():
        html += f"<tr><td><b>{key}</b></td><td>{value}</td></tr>"
    html += "</table></body></html>"
    return html

if __name__ == "__main__":
    info = get_system_info()
    report = generate_html_report(info)

    with open("testreport.html", "w") as file:
        file.write(report)

    print("System report generated: system_report.html")
