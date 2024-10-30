from netmiko import ConnectHandler
import os 
import difflib

def ssh(connection):
    print('---Connecting to SSH---')
############################################ASK FOR DEVICE INFO ######################################

    while True:
        device_type = input("Enter the device type (default is cisco_ios): ") or 'cisco_ios'
        if device_type.strip(): ## strips input to what is actually entered so if nothing is entered it will go to the else statement
            break
        else:
            print("Device type cannot be empty. Please enter a valid device type.")


    # Validates ip address entered to make sure it has 3 dots and ranges from 0.0.0.0 to 255.255.255.255
    while True:
        host = input("Enter the host IP address: ").strip()
        if host.count('.') == 3 and all(map(str.isdigit, host.split('.'))) and 0 <= int(
                host.split('.')[0]) <= 255 and 0 <= int(host.split('.')[1]) <= 255 and 0 <= int(
                host.split('.')[2]) <= 255 and 0 <= int(host.split('.')[3]) <= 255:
            break
        else:
            print("Invalid IP address. Please enter a valid IP address.")

    ## Validates if username is not empty or only contains whitespace
    while True:
        username = input("Enter the username: ")
        if username.strip(): ## strips input to what is actually entered so if nothing is entered it will go to the else statement
            break
        else:
            print("Username cannot be empty. Please enter a valid username.")


    # No need for validation as password can be empty and can contain leading or trailing whitespaces
    password = input("Enter the password: ")

    secret = input("Enter the enable secret (optional, press Enter to skip): ") or '' # no input means it will be skipped

######### USE DEVICE INFO ##########
    
    cisco_device = {
        'device_type': device_type,#'cisco_ios'#
        'host': host,
        'username': username,
        'password': password,
        'port': 22, # since ssh was selected no need to ask for the port
        'secret': secret,
    }
    print(cisco_device)
    try:
        connection = ConnectHandler(**cisco_device)
        print(f"Connected to {host} successfully.")
        return connection

    except Exception as e:
        print(f"Failed to connect to {host}: {e}")# Displays error from netmiko
        return None

    finally:  # will always run
        connection.disconnect()


def run_hard(connection):
    'Compare the current running configuration of a network device against the Cisco device hardening advice. This can be found on the Moodle page.'
    print ('---Comparing Running Configuration---')
    run_config = connection.send_command('show run')
    start_run = connection.send_command('show start')

    with open('running_configuration.txt', 'w') as run_file:
        run_file.write(run_config)

    with open('startup_configuration.txt', 'w') as start_file:
        start_file.write(start_run)

    diff = difflib.unified_diff(
        run_config.splitlines(),
        start_run.splitlines(),
        fromfile = 'Running-configuation',
        tofile='startup_configuration',
        lineterm=''
    )

    print('\n'.join(list(diff)))

    hardening_checks = {
        "SSH enabled": "ip ssh version 2",
        "Telnet disabled": "no service telnet",
        "Password encryption": "serivce password-ecnryption"
    }

    def check_hardening(run_config):
        for check, rule, in hardening_checks.items():
            if rule in run_config:
                print(f"[Pass] {check}")
            else:
                print(f"[Fail] {check}")
    
    check_hardening(run_config)
    



def syslog(connection):
    'Configure the network device to enable syslog to allow for event logging and monitoring'


def main(connection):
    ssh(connection)
    try:
        while True:
            choice = input("a. Compare the running configuration to cisco's hardening advice?\nb. Configure the network device to enable syslog\nc. Quit\nSelect a, b or c: ").strip().lower()
            if choice == "a":
                run_hard(connection)

            elif choice == "b":
                syslog(connection)

            elif choice == "c":
                break

            else:
                print("Invalid input, please try again")

    except:
        print("An error occured")


if __name__ == '__main__':
    connection=None
    main(connection)
