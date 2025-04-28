import os
import datetime
from netmiko import ConnectHandler

# Read device IPs from file
with open("wlc_diff", "r") as file:
    device_ips = [line.strip() for line in file]

# Credentials stored in the script
username = "Netbackup"
password = "NetAutoBup@10"

# Command to execute
command = "show run-config startup-commands"  # Modify as needed

# Ensure the directory exists
output_dir = "/data/ftpusr006/WLC/"
os.makedirs(output_dir, exist_ok=True)

print(f"Saving outputs to {output_dir}\n")

# Loop through devices and execute command
for host in device_ips:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{output_dir}{host}_{timestamp}.cfg"  # IP-based filename

    try:
        print(f"Connecting to {host}...")
        device = {
            "device_type": "cisco_wlc",
            "host": host,
            "username": username,
            "password": password,
        }
        net_connect = ConnectHandler(**device)
        print(f"Executing command on {host}...")
        output = net_connect.send_command(command)
        print(f"Command executed successfully on {host}.")

        # Save output to per-device file
        with open(output_file, "w") as file:
            file.write(f"Device {host} Output:\n{output}\n\n")

        net_connect.disconnect()
    except Exception as e:
        error_message = f"Error connecting to {host}: {e}"
        print(error_message)
        with open(output_file, "w") as file:
            file.write(error_message + "\n\n")  # Log errors to file

print("\nExecution complete! Each device's output saved separately.")
