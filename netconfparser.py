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
                print("NETCONF is disabled on this device, configure it with \"netconf-yang\" and wait some minutes before verifying again.")
                continue
            if "datastore" in line:
                self.datastore = re.compile("(?<=datastore:).*").search(line).group().strip()
            if "ssh" in line:
                self.sshport = re.compile("(?<=ssh port:).*").search(line).group().strip()

class yangprocess:
    def __init__(self, devicename):
        self.devicename = devicename
        self.status = None          #Netconf status enabled or not
        self.nesd = None            #nesd status enabled or not
        self.syncfd = None          #syncfd status enabled or not
        self.ncsshd = None          #ncsshd status enabled or not
        self.dmiauthd = None        #dmiauthd status enabled or not
        self.nginx = None          #ncsshd status enabled or not
        self.ndbmand = None         #ndbmand status enabled or not
        self.pubd = None            #pubd status enabled or not

    def netconfparser(self, service):

        nconfst_cmd = "show platform software yang-management process state"
        nconfst_opt = radkit_cli.get_any_single_output(self.devicename,nconfst_cmd,service)
        print(nconfst_opt)
        for line in nconfst_opt.splitlines():
            print(line)
            if "Confd Status: Started" in line:
                self.status = "Started"
            if "Confd Status: Not Running" in line:
                print("NETCONF is disabled on this device, configure it with \"netconf-yang\" and wait some minutes before verifying again.")
                continue
            if "nesd" and "Running" and "Active" in line:
                self.nesd = "Running and Active"
            if "nesd" and "Not Running" or "Down" in line:
                print("Process nesd is Not Running or Down")
                continue
            if "syncfd" and "Running" and "Active" in line:
                self.syncfd = "Running and Active"
            if "syncfd" and "Not Running" or "Down" in line:
                print("Process syncfd is Not Running or Down")
                continue
            if "ncsshd" and "Running" in line:
                self.ncsshd = "Running"
            if "ncsshd" and "Not Running" in line:
                print("Process ncsshd is Not Running")
                continue
            if "dmiauthd" and "Running" and "Active" in line:
                self.dmiauthd = "Running and Active"
            if "dmiauthd" and "Not Running" or "Down" in line:
                print("Process dmiauthd is Not Running or Down")
                continue
            if "nginx" and "Running" in line:
                self.nginx = "Running"
            if "nginx" and "Not Running" or "Down" in line:
                print("Process nginx is Not Running or Down")
                continue
            if "ndbmand" and "Running" and "Active" in line:
                self.ndbmand = "Running and Active"
            if "ndbmand" and "Not Running" or "Down" in line:
                print("Process ndbmand is Not Running or Down")
                continue
            if "pubd" and "Running" and "Active" in line:
                self.pubd = "Running and Active"
            if "pubd" and "Not Running" in line:
                print("Process pubd is Not Running")