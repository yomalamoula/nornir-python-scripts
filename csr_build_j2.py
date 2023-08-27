import getpass
from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml
from jinja2 import Environment, FileSystemLoader
from tqdm import tqdm
import csv
#importing python libraries

nr = InitNornir(config_file="config5.yml")
#The above line is telling nornir where the config file is located
user = input("Please enter your username: ")
password = getpass.getpass(prompt="Please enter your password: ")
nr.inventory.defaults.username = user
nr.inventory.defaults.password = password
#The above lines will prompt the user to enter their username and password and use that input to connect to the devices.

"""
Prompting user for hostname
"""
target = input("Enter the hostname of the device you wish to configure: ")
target_host = nr.filter(name=target)

def load_vars(task, progress_bar):
    progress_bar.update()
# above line is creating a function called load_vars and also a progress bar
    data = task.run(task=load_yaml, file=f"./host_vars/{task.host}.yaml")
# above line is creating a variable called data and linking it to the host specific yaml files in host_vars folder
    task.host["facts"] = data.result
# above line is going to bine the render template to a dictionayr key called facts and link it to the results of data
    csr_template(task)
# above line is going to call the function ospf_templates below

def csr_template(task):
# above line is creating a function called snmp_tempate
    template = task.run(task=template_file, template="csr_buildtemplate.j2", path="./templates")
# above line is creating a variable called template and linking template to the jinja2 file csr_buildtemplate.j2 and providing the path to the file
    task.host["csr1_config"] = template.result
# above line is going to bind the render template to a dictionary key and linking it to the results of template
    rendered = task.host["csr1_config"]
# above line is creating a new variable called rendered and making it equal to task host ospf_config
    configuration = rendered.splitlines()
# above line is going create the variable configuratoin, render the data and break it down line by line
    task.run(task=send_configs, configs=configuration)
# above line is going to use task.run to call send_configs and send the config from the configuration variable 

with tqdm(total=len(nr.inventory.hosts)) as progress_bar:
    results = nr.run(task=load_vars, progress_bar=progress_bar)
# above is going to use tqdm to create a progress bar to show script progress as it pushes the config out to each host

print_result(results)
# finally we are creating the variable results which is going to collate the results of the test_template function
# and print the results to screen
