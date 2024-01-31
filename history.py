from netmiko import ConnectHandler
from datetime import datetime

def execute_command(host, username, password, device_type, command):
    # Create a dictionary with device information
    device = {
        'device_type': device_type,
        'ip': host,
        'username': username,
        'password': password,
    }

    try:
        # Connect to the router
        with ConnectHandler(**device) as ssh:
            # Execute the command with terminal length set to 0
            command_with_terminal_length = f"{command}"
            ssh.send_command("terminal length 0")
            output = ssh.send_command(command_with_terminal_length)

        return output
    except Exception as e:
        print(f"Error: {e}")

def filter_commands(output, commands_to_filter):
    # Split the output into lines
    output_lines = output.splitlines()

    # Filter out lines containing specified commands
    filtered_output = [line for line in output_lines if not any(cmd in line for cmd in commands_to_filter)]

    return "\n".join(filtered_output)

def read_commands_from_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def save_to_file(output, host):
    # Generate a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Construct the filename based on hostname and timestamp
    filename = f"{host}_{timestamp}.txt"

    # Save the output to a .txt file
    with open(filename, "w") as file:
        file.write(output)

    print(f"Output saved to {filename}")

# Example usage
router_host = "135.25.14.101"
router_username = "CISCO15"
router_password = "otbu+1"
router_device_type = "cisco_ios"  # Adjust based on your router type
command_to_execute = "show history all"

# List of commands to filter
commands_to_filter = read_commands_from_file("filter_commands.txt")

# Execute the command on the router using Netmiko
output = execute_command(router_host, router_username, router_password, router_device_type, command_to_execute)

# Filter the output
filtered_output = filter_commands(output, commands_to_filter)

# Save the results to a .txt file
save_to_file(filtered_output, router_host)

# Display the results
print("Original Output:")
print(output)
print("\nFiltered Output:")
print(filtered_output)