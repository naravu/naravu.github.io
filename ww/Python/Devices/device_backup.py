#!/usr/bin/python3.8
from netmiko import ConnectHandler
import os
from datetime import datetime

# Function to define device parameters
def create_device(host, username, password):
    return {
        "device_type": "cisco_ios",  # Update this based on your device type
        "host": host,
        "username": username,
        "password": password,
        "timeout": 30,
    }

# Execute a command on the remote device and write output to file
def execute_and_save(ssh_connection, command, host, output_dir):
    try:
        print(f"Executing command on {host}: {command}")
        output = ssh_connection.send_command(command)

        # Generate filename with device name and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{host}_{timestamp}.cfg"
        full_path = os.path.join(output_dir, filename)

        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")

        # Save the output to the file
        with open(full_path, "w") as file:
            file.write(output)
        print(f"Output saved to {full_path}")
    except Exception as e:
        print(f"Failed to execute command on {host}: {e}")

# Main function to connect to devices and perform tasks
def process_devices(device_file, username, password, command, output_dir):
    try:
        with open(device_file, "r") as file:
            for line in file:
                host = line.strip()
                if not host:
                    continue

                print(f"\nConnecting to device {host}...")
                device_params = create_device(host, username, password)
                try:
                    # Establish SSH connection
                    ssh_connection = ConnectHandler(**device_params)

                    # Execute command and save output
                    execute_and_save(ssh_connection, command, host, output_dir)

                except Exception as e:
                    print(f"Failed to process {host}: {e}")
                finally:
                    # Ensure SSH connection is closed
                    ssh_connection.disconnect()
                    print(f"Disconnected from {host}.")
    except FileNotFoundError:
        print(f"Device file {device_file} not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Variables
username = "Netbackup"
password = "NetAutoBup@10"
device_file = "./DKVI.new"  # Update with the path to your device list file
command = "show running-config"  # Command to be executed on devices
output_dir = "/data/ftpusr006/WLC/"  # Directory to save output files

if __name__ == "__main__":
    process_devices(device_file, username, password, command, output_dir)
