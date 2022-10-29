""" This script will create a data and voice VLAN on a switch based on user input.
The script will prompt the user for their credentials, then for the switchport they want configuring, 
it will request the Data VLAN ID, the Voice VLAN id and then configure the devices in the configuration file. 
It will finally save the configuration to startup. 
Note: if no Voice VLAN is provided the command will still run but no voice VLAN will be enabled.
"""

import getpass
from time import sleep
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config, netmiko_send_command
from nornir_utils.plugins.functions import print_result
#importing netmiko send_config library

nr = InitNornir(config_file="config3.yml")
#The above line is telling nornir where the config file is located
user = input("Please enter your username: ")
password = getpass.getpass(prompt="Please enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.


switchport = input("Please enter Switch port number you wish to configure (example: 0/1): ")
vlanid = input("Please enter the Data VLAN number you wish to enable on the port (example 10): ")
voicevlan = input("Please enter the Voice VLAN you wish to enable on the port or leave blank if Voice is not required): ")


def send_config_test(task):
    task.run(task=netmiko_send_config, config_commands=[
        f"interface ethernet{switchport}",
        f"switchport access vlan {vlanid}",
        f"switchport voice vlan {voicevlan}",
        "do wr mem"])

#function is sending the configuration commands to the hosts

def show_vlan(task):
    task.run(task=netmiko_send_command, command_string="show vlan")
              
config_results = nr.run(task=send_config_test)
vlan_results = nr.run(task=show_vlan)
print_result(config_results)
print_result(vlan_results)
#setting the object results to output of the send_config_test function
