#Script Name : nxapilibpy.py
#Script Purpose or Overview : This python file contains basic nutanix api method to connect Nutanix Prism Element
#This file is developed by Taeho Choi(taeho.choi@nutanix.com) by referring below resources
#
#   disclaimer
#	This code is intended as a standalone example.  Subject to licensing restrictions defined on nutanix.dev, this can be downloaded, copied and/or modified in any way you see fit.
#	Please be aware that all public code samples provided by Nutanix are unofficial in nature, are provided as examples only, are unsupported and will need to be heavily scrutinized and potentially modified before they can be used in a production environment.  
#   All such code samples are provided on an as-is basis, and Nutanix expressly disclaims all warranties, express or implied.
#	All code samples are © Nutanix, Inc., and are provided as-is under the MIT license. (https://opensource.org/licenses/MIT)

import json,sys
import time
import requests
import base64
import urllib3
import ipaddress
import getpass
import os.path
import sys
from pathlib import Path
from urllib.parse import quote
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ========== DO NOT CHANGE ANYTHING UNDER THIS LINE =====
class my_api():
    def __init__(self,ip,username,password):

        # Cluster IP, username, password.
        self.ip_addr = ip
        self.username = username
        self.password = password

        # Base URL at which v0.8 REST services are hosted in Prism Gateway.
        base_urlv08 = 'https://%s:9440/PrismGateway/services/rest/v0.8/'
        self.base_urlv08 = base_urlv08 % self.ip_addr

        # Base URL at which v1 REST services are hosted in Prism Gateway.
        base_urlv1 = 'https://%s:9440/PrismGateway/services/rest/v1/'
        self.base_urlv1 = base_urlv1 % self.ip_addr

        # Base URL at which v2 REST services are hosted in Prism Gateway.
        base_urlv2 = 'https://%s:9440/PrismGateway/services/rest/v2.0/'
        self.base_urlv2 = base_urlv2 % self.ip_addr

        # Base URL at which v3 REST services are hosted in Prism Gateway.
        base_urlv3 = 'https://%s:9440/PrismGateway/services/rest/v3/'
        self.base_urlv3 = base_urlv3 % self.ip_addr

        self.session = self.get_server_session(self.username, self.password)    

    def get_server_session(self, username, password):

        # Creating REST client session for server connection, after globally
        # setting authorization, content type, and character set.
        session = requests.Session()
        session.auth = (username, password)
        session.verify = False
        session.headers.update({'Content-Type': 'application/json; charset=utf-8'})
        return session

    # Get all entity uuid table first except cluster 
    def get_all_entity_info(self,ent):
        if (ent == "hosts"):
            cluster_url = self.base_urlv2 + "hosts/"
        elif (ent == 'vms'):
            cluster_url = self.base_urlv1 + "vms/"
        elif (ent == 'images'):
            cluster_url = self.base_urlv2 + "images/"
        elif (ent == 'ctr'):
            cluster_url = self.base_urlv2 + "storage_containers/"
        elif (ent == 'net'):
            cluster_url = self.base_urlv2 + "networks/"
        elif (ent == 'cluster'):
            cluster_url = self.base_urlv1 + "cluster/"
        elif (ent == 'disk'):
            cluster_url = self.base_urlv2 + "disks/"
        else: 
            print("wrong entiry parsed")    
        print("API endpoint is: {}\n".format(cluster_url))
        server_response = self.session.get(cluster_url)
        try:
            return_body = json.loads(server_response.text)
        except ValueError:
            sys.exit("Hmm somethig went wrong, is passwd ok? is user unlocked?")
        return server_response.status_code ,return_body

        # Get entity information.
    def get_single_ent_info(self,ent,uuid):
        if (ent == "hosts"):
            cluster_url = self.base_urlv2 + "hosts/"+uuid
        elif (ent == 'vms'):
            cluster_url = self.base_urlv1 + "vms/"+uuid
        elif (ent == 'images'):
            cluster_url = self.base_urlv2 + "images/"+uuid
        elif (ent == 'ctr'):
            cluster_url = self.base_urlv2 + "storage_containers/"+uuid
        elif (ent == 'net'):
            cluster_url = self.base_urlv2 + "networks/"+uuid
        elif (ent == 'subnet'):
            cluster_url = self.base_urlv2 + "networks/"+uuid+"/addresses"
        elif (ent == 'tasks'):
            cluster_url = self.base_urlv2 + "tasks/"+uuid
        elif (ent == 'ncc'):
            cluster_url = self.base_urlv1 + "ncc/"+uuid
        else: 
            print("wrong entiry parsed")
        print(cluster_url)
        server_response = self.session.get(cluster_url)
        try:
            return_body = json.loads(server_response.text)
        except ValueError:
            sys.exit("Hmm somethig went wrong, is passwd ok? is user unlocked?")
        return server_response.status_code ,return_body
    
    # Get resource stats.
    def get_resource_stats(self,ent_type,uuid,resource,period,interval):
        period = 3600*period
        if (resource == "cpu"):
            metric = "hypervisor_cpu_usage_ppm"
        elif (resource == "mem"):
            if (ent_type == "host"):
                metric = "hypervisor_memory_usage_ppm"
            elif (ent_type == "vm"):
                metric = "guest.memory_usage_ppm"

        if ent_type == "vm":
            cluster_url = self.base_urlv1 + "vms/" + uuid + "/stats/?metrics=" + metric + "&startTimeInUsecs="
        elif ent_type == "host":
            cluster_url = self.base_urlv1 + "hosts/" + uuid + "/stats/?metrics=" + metric + "&startTimeInUsecs="
        else: 
            print("Selected wrong entity type...")
            print ("Existing")

        cur_time = int(time.time())
        start_time = cur_time - period
        # Now convert to usecs.
        cur_time = cur_time * 1000000
        start_time = start_time * 1000000

        # From: https://www.nutanix.dev/2019/09/23/getting-vm-performance-metrics-via-api/
        # https://10.133.16.50:9440/api/nutanix/v1/vms/3aa1699a-ec41-4037-aade-c73a9d14ed8c/stats/?metrics=hypervisor_cpu_usage_ppm&startTimeInUsecs=1524009660000000&endTimeInUsecs=1524096060000000&interval=30
 
        cluster_url += str(start_time) + "&" + "endTimeInUsecs=" + str(cur_time) + "&interval="+str(interval)
        server_response = self.session.get(cluster_url)
        return server_response.status_code ,json.loads(server_response.text)

    # Post new ent.
    def post_new_ent(self,ent,body):
        if (ent == "image"):
            cluster_url = self.base_urlv08 + "images"
            server_response = self.session.post(cluster_url,data = json.dumps(body))

        elif (ent == "eula"):
            cluster_url = self.base_urlv1 + "eulas/accept"
            server_response = self.session.post(cluster_url,data = json.dumps(body))

        elif (ent == "pulse"):
            cluster_url = self.base_urlv1 + "pulse"
            server_response = self.session.put(cluster_url,data = json.dumps(body))

        elif (ent == "pubkey"):
            cluster_url = self.base_urlv2 + "cluster/public_keys"
            server_response = self.session.post(cluster_url,data = json.dumps(body))
        
        elif (ent == "ntp"):
            cluster_url = self.base_urlv2 + "cluster/ntp_servers"
            server_response = self.session.post(cluster_url,data = json.dumps(body))
        
        elif (ent == "dns"):
            cluster_url = self.base_urlv1 + "cluster/name_servers"
            server_response = self.session.post(cluster_url,data = json.dumps(body))

        elif (ent == "net"):
            cluster_url = self.base_urlv08 + "networks"
            server_response = self.session.post(cluster_url,data = json.dumps(body))

        elif (ent == 'ncc'):
            cluster_url = self.base_urlv1 + "ncc/checks"
            server_response = self.session.post(cluster_url,data = json.dumps(body))

        elif (ent == "man_net"):
            cluster_url = self.base_urlv08 + "networks"
            server_response = self.session.post(cluster_url,data = json.dumps(body))

        elif (ent == "passwd"):
            cluster_url = self.base_urlv1 + "users/change_password"
            server_response = self.session.put(cluster_url,data = json.dumps(body))

        else:
            print("Wrong selection")
        
        return server_response.status_code ,json.loads(server_response.text)

    # Create new VM with disk.
    def create_vm(self,body):
        cluster_url = self.base_urlv2 + "vms?include_vm_disk_config=true&include_vm_nic_config=true"
        print(json.dumps(body))
        server_response = self.session.post(cluster_url,data = json.dumps(body))
        return server_response.status_code ,json.loads(server_response.text)
    
    # Delete VM.
    def delete_vm(self,body,vm_uuid):
        cluster_url = self.base_urlv2 + "vms/" + vm_uuid
        server_response = self.session.delete(cluster_url,data = json.dumps(body))
        return server_response.status_code ,json.loads(server_response.text)
    
    # Attach disk to VM.
    def attach_disk(self,body,vm_uuid):
        cluster_url = self.base_urlv2 + "vms/" + vm_uuid + "/disks/attach"
        server_response = self.session.post(cluster_url,data = json.dumps(body))
        return server_response.status_code ,json.loads(server_response.text)
    
    # VM power operataion
    def vm_powerop(self,body,vm_uuid):
        cluster_url = self.base_urlv2 + "vms/" + vm_uuid + "/set_power_state/"
        print(json.dumps(body))
        server_response = self.session.post(cluster_url,data = json.dumps(body))
        return server_response.status_code ,json.loads(server_response.text)

    # print all ent list with pretty format
    def print_all_ent(self,ent):
        if (ent == "hosts"):
            # 1. Collect all current vm uuids
            status, all_ent = self.get_all_entity_info("hosts")
            # 2. Check the longest host name size to align print format
            hostName=[]
            for i in all_ent["entities"]:
                hostName.append(i["name"])
            maxfield = len(max(hostName,key=len))
            # 2.5 Sorting the dictionary with name
            all_ent["entities"] = sorted(all_ent["entities"], key=lambda a:a["name"])
            # 3. Display all host name and uuid for user to select host by uuid
            for n in all_ent["entities"]:
        	    print("Host name: " + n["name"].ljust(maxfield+2)+" uuid: " + n["uuid"].rjust(30))
            # 4. Creating valid UUid list and compare whether input is valid
            hostUUid=[]
            for i in all_ent["entities"]:
                hostUUid.append(i["uuid"])
            return status,hostUUid
            
        elif (ent == 'vms'):
            # 1. Collect all current vm uuids 
            status, all_ent = self.get_all_entity_info("vms")
            # 2. Check the longest VM name size to align print format
            vmName=[]
            for i in all_ent["entities"]:
                vmName.append(i["vmName"])
            maxfield = len(max(vmName,key=len)) 
            # 2.5 Sorting the dictionary with vmName
            all_ent["entities"] = sorted(all_ent["entities"], key=lambda a:a["vmName"])
            # 3. Display all vm name and uuid for user to select VM by uuid
            for n in all_ent["entities"]:
                print("VM name: " + n["vmName"].ljust(maxfield+2)+" uuid: " + n["uuid"].ljust(40)+ "power:"+n["powerState"])
            # 4. Creating valid UUid list and compare whether input is valid
            vmUUid=[]
            for i in all_ent["entities"]:
                vmUUid.append(i["uuid"])
            return status,vmUUid

        elif (ent == 'images'):
            # 1. Get the UUID of all imgs.
            status, all_ent = self.get_all_entity_info("images")

            # 2. Check the longest img name size to align print format
            imgName=[]
            for i in all_ent["entities"]:
                imgName.append(i["name"])
            maxfield = len(max(imgName,key=len))

            imgType=[]
            for i in all_ent["entities"]:
                imgType.append(str(i.get("image_type")))
            imgmaxfield = len(max(imgType,key=len))

            # 2.5 Sorting the dictionary with name
            all_ent["entities"] = sorted(all_ent["entities"], key=lambda a:a["name"])

            # 3. Display all img name, uuid, img_type: ISO or disk
            for n in all_ent["entities"]:
                print("Image name: " + n["name"].ljust(maxfield+2)+" uuid: " + n["uuid"] +" vm_disk_id: " + str(n.get("vm_disk_id")).ljust(40) + "  image_type: "+ str(n.get("image_type")).ljust(imgmaxfield+2))
            # 4. Creating valid UUid list and compare whether input is valid
            imgUUid=[]
            for i in all_ent["entities"]:
                imgUUid.append(i["uuid"])
            return status,imgUUid
          
        elif (ent == 'ctr'):
            # 1. Get the UUID of container 
            status, all_ent = self.get_all_entity_info("ctr")
            # 2. Check the longest ctr name size to align print format
            ctrName=[]
            for i in all_ent["entities"]:
                ctrName.append(i["name"])
            maxfield = len(max(ctrName,key=len))
            # 2.5 Sorting the dictionary with name
            all_ent["entities"] = sorted(all_ent["entities"], key=lambda a:a["name"])
            # 3. Display all ctr name, uuid, img_type: ISO or disk
            for n in all_ent["entities"]:
                print("Container name: " + n["name"].ljust(maxfield)+" storage_container_uuid: " + n["storage_container_uuid"].ljust(40))
            # 4. Creating valid UUid list and compare whether input is valid
            ctrUUid=[]
            for i in all_ent["entities"]:
                ctrUUid.append(i["storage_container_uuid"])
            return status,ctrUUid
            
        elif (ent == 'net'):
            # 1. Get the UUID of network 
            status, all_ent = self.get_all_entity_info("net")

            # 2. Check the longest ctr name size to align print format
            netName=[]
            for i in all_ent["entities"]:
                netName.append(i["name"])
            maxfield = len(max(netName,key=len))

            # 2.5 Sorting the dictionary with name
            all_ent["entities"] = sorted(all_ent["entities"], key=lambda a:a["name"])

            # 3. Display all ctr name, uuid, img_type: ISO or disk
            for n in all_ent["entities"]:
                print("Network name: " + n["name"].ljust(maxfield)+" network uuid: " + n["uuid"] + "  vlan: "+ str(n["vlan_id"]).ljust(6)+"  dhcp option:" + str(n["ip_config"]["dhcp_options"]))
            # 4. Creating valid UUid list and compare whether input is valid
            netUUid=[]
            for i in all_ent["entities"]:
                netUUid.append(i["uuid"])
            return status,netUUid
    
        else: 
            print("wrong entiry parsed")

    def EntityMenu(self,clustername,ip,username):
        print('#'*80)
        print("Be aware you are in {} cluster({}) as {} user".format(clustername,ip,username))
        print("What kind of operation do you want?\n")
        print('#'*4 + " MENU " + '#'*4+'\n'  )
        print("Type 0: Check specific task status")
        print("Type 1: Cluster info")
        print("Type 2: Host info")
        print("Type 3: Vm info")
        print("Type 4: Image info")
        print("Type 5: Container info")
        print("Type 6: Network info")
        print("Type 7: Upload new image from URL")
        print("Type 8: Create new VM from disk image with cloud-init(bulk opt)")
        print("Type 9: VM Power on/off operation(bulk opt)")
        print("Type 10: Delete VM operation")
        print("Type 11: Performance data(cpu/mem) for VM or host")
        print("Type 12: Cluster disk detail info")
        print("Type 13: New cluster setup - EULA,Pulse,NTP etc")
        print("Type 14: Run new ncc health checks")
        print("Type 15: Create new managed network(ip pool)")
        print("Type 16: Change admin user password")
        print("Type q: Exit program \n")
        print('#'*80)
        seLection = input()
        return seLection

    def GetUUid(self):
        uuid = input("\n\nEnter entity uuid(ex.vm,host,image...) to see the detail: \n")
        if uuid == "":
            print("You pressed enter")
            return str(1)
        else:
            print("You typed uuid: %s" %uuid)
            return uuid

    def NewPasswd(self,rawpass):
        home = str(Path.home())
        cluster_config = home+"/.nx/config"
        #Encoding passwd 
        benc_passwd                 =       base64.b64encode(rawpass.encode("utf-8"))
        #Convert byte format to string to send json
        newpass                     =       benc_passwd.decode("utf-8")
        #load config file from existing one
        with open(cluster_config,'r') as old_file:
            config = json.load(old_file)
        #update passwd
        config["password"] = newpass 
        #write passwd to config  
        with open(cluster_config,'w') as new_file:
            json.dump(config, new_file)
        return print("\n %s passwd has been updated !!\n" %config["cluster_name"])
 
# ========== DO NOT CHANGE ANYTHING ABOVE THIS LINE =====
    
def GetClusterDetail():
    #Get current user home directory
    home = str(Path.home())
    # .nx for configuration folder
    path = home+"/.nx"
    #Cluster config file in json format
    cluster_config = home+"/.nx/config"
        
    if os.path.exists(cluster_config) == False:
        print("\nNo cluster config file found, will create new config file now\n")
        try:
            os.mkdir(path)
        except OSError:
            print("%s directory creation failed" %path)
        else:
            print("%s directory creation is suceeded" %path)

        config={}
        config["cluster_name"]      =       input("What is cluster name?: ")    
        while True:  
            config["ip"]            =       input("What is Prism Element IP?: ")
            try : 
                ipaddress.ip_address(config["ip"])
                break
            except ValueError:
                print ("it doens't look like right ip address format")
        config["username"]          =       input("Prism admin role username: ")
        raw_passwd                  =       getpass.getpass(prompt="Password for admin user?\n" , stream=None)
        #Encoding passwd 
        benc_passwd                 =       base64.b64encode(raw_passwd.encode("utf-8"))
        #Convert byte format to string to send json
        config["password"]          =       benc_passwd.decode("utf-8")
        with open(cluster_config,'w') as out_file:
            json.dump(config,out_file)
        print("\n %s config file has been created !!\n" %config["cluster_name"])
        return(config["cluster_name"],config["ip"],config["username"],raw_passwd)

    else :
        print("Reading your config...")
        with open(cluster_config) as in_file:
            config = json.load(in_file)
            ip = config["ip"]
            username = config["username"]
            enc_passwd = config["password"]
            password = base64.b64decode(enc_passwd).decode("utf-8")
            cluster_name = config["cluster_name"]
        print("Found {} cluster config file in {}\n".format(cluster_name,cluster_config))
        return (cluster_name,ip,username,password)