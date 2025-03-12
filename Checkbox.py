import logging
from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor
from networkCommands import get_commands
from tkinter import Tk, Label, ttk, Button, StringVar, Checkbutton, Entry

# Configure logging settings (optional)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='app.log')

class CustomDialog:
    def __init__(self, title, prompt_ip, prompt_user, prompt_pass, options, current_username='cisco15', width=300, height=800):
        self.root = Tk()
        self.root.title(title)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_position = (screen_width - width) // 2
        y_position = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x_position}+{y_position}")
        # current_username = self.get_username()
        self.selected_ips = []
        self.username_var = StringVar(value='abc')
        self.password_var = StringVar()

        Label(self.root, text=prompt_ip).pack()

        for ip in options:
            var = StringVar(value='off')
            Checkbutton(self.root, text=ip, variable=var, onvalue='on', offvalue='off', command=lambda i=ip: self.toggle_ip(i)).pack()

        Label(self.root, text=prompt_user).pack()
        Entry(self.root, textvariable=self.username_var).pack()

        Label(self.root, text=prompt_pass).pack()
        Entry(self.root, textvariable=self.password_var, show='*').pack()

        Button(self.root, text="OK", command=self.ok).pack()

    def toggle_ip(self, ip):
        if ip in self.selected_ips:
            self.selected_ips.remove(ip)
        else:
            self.selected_ips.append(ip)

    def get_username(self):
        # Retrieve username and password from the networkCommands module
        network_commands = get_commands('username')
        return network_commands
    def ok(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()


class RouterManager:
    def __init__(self, ip, username, password):
        # Initialize the device parameters
        self.device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': username,
            'password': password,
        }

    def establish_connection(self):
        # Establish an SSH connection using Netmiko
        return ConnectHandler(**self.device)


    def get_username(self):
        # Retrieve username and password from the networkCommands module
        network_commands = get_commands('username')
        return network_commands

    def run_script_for_ip(self, ip):
        # Your existing script logic here
        # Update self.device['ip'] with the selected IP
        self.device['ip'] = ip

        try:
            with self.establish_connection() as ssh_conn:
                # ... your existing script logic ...
                commands = get_commands('file_prompt')
                logging.info("Script started.")
                for command in commands:
                    logging.info(command)
        except Exception as e:
            logging.error(f"Error for IP {ip}: {e}")

    def main(self):
        root = Tk()
        root.withdraw()
        logging.info("Script started.")

        # Retrieve the list of router IPs from the networkCommands module
        router_ips = get_commands('router_ip')
        current_username = self.get_username()

        # Create a dialog box to get input
        dialog = CustomDialog("Input", "Select router IP address:", f"Enter username:", "Enter password:", router_ips)
        dialog.run()

        selected_ips = dialog.selected_ips
        username = dialog.username_var.get(current_username)
        password = dialog.password_var.get()

        try:
            # Run the script for each selected IP in parallel
            with ThreadPoolExecutor() as executor:
                executor.map(self.run_script_for_ip, selected_ips)

        except Exception as e:
            logging.error(f"Error in parallel execution: {e}")

        try:
            # Establish an SSH connection
            with self.establish_connection() as ssh_conn:
                logging.info('Connecting to: ' + username)
        except Exception as e:
            logging.error(f"Error in parallel execution: {e}")


if __name__ == "__main__":
    # Instantiate the RouterManager class and call the main method
    router_manager = RouterManager(ip='', username='', password='')
    router_manager.main()
