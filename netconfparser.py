from dataclasses import dataclass
import radkit_client
import ipaddress
import re
import sys
import radkit_cli
import ipverifications

class netconfstatus:
    def __init__(self, devicename):
        self.devicename = devicename 
        self.status = None          #Netconf status enabled or not
        self.datastore = None       #Candidate Datastore must be disabled
        self.sshport = None         #Must be 830
        self.outrpcerrors = None    
        self.droppedsessions = None

    def netconfparser(self, service):

        nconfst_cmd = "show netconf-yang status"
        nconfst_opt = radkit_cli.get_any_single_output(self.devicename,nconfst_cmd,service)

        for line in nconfst_opt.splitlines():
            if "netconf-yang: enabled" in line:
                self.status = "Enabled"
            if "netconf-yang: disabled" in line:
                sys.exit("NETCONF is disabled on this device, configure it with \"netconf-yang\" and wait some minutes before verifying again.")
            if "datastore" in line:
                self.datastore = re.compile("(?<=datastore:).*").search(line).group().strip()
            if "ssh" in line:
                self.sshport = re.compile("(?<=ssh port:).*").search(line).group().strip()
