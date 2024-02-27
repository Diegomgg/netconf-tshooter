from dataclasses import dataclass
import radkit_client
import ipaddress
import re
import sys
import radkit_cli
import ipverifications
import netconfparser

from radkit_client.sync import (
    create_context
)

def startup():
    email = "digranad@cisco.com"
    domain = "PROD"
    string = "vh2a-6ow9-8tqk"
    service = radkit_cli.radkit_login(email,domain,string)
    return (service)

def initial_setup():
    hosts = []
    cont = True
    while cont:
        print("Please add a device to be reviewed regarding Netconf")
        device_source_ip = ipverifications.ip_validator_input("Inventory Management IP for the device ")
        hosts.append(device_source_ip)
        print("Do you want to add another device?")
        res = input("Yes or No > ")
        if res == "No":
            cont = False
            break
        
    
    #hosts = ['172.12.0.3', '172.12.0.4']
    for i in hosts:
        hostname = radkit_cli.find_device(service, i)

        print ("Validating NETCONF Status for Device "+hostname)
        ncstat = netconfparser.netconfstatus(hostname)
        ncstat.netconfparser(service)
        print (ncstat.__dict__)
        '''
    '''
if __name__ == "__main__":
    with create_context():
        global service

        service = startup()
        initial_setup()
