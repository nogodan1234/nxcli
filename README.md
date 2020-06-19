# nxcli

*  Script Name : nxcli
*  Script Purpose or Overview
*  - This program is python api client for Nutanix Prism Element(not Prism Central)
*  - This program can collect overall cluster information and statstics info
*  - This program relies on certain python packages and function in nxapilib.py
*
*  This file is developed by Taeho Choi(taeho.choi@nutanix.com) by referring below resources
*  For reference look at:
*  https://www.digitalformula.net/2018/api/vm-performance-stats-with-nutanix-rest-api/
*  https://github.com/nelsonad77/acropolis-api-examples
*  https://github.com/sandeep-car/perfmon/
*
*   Disclaimer
*   This code is intended as a standalone example.
*   Subject to licensing restrictions defined on nutanix.dev,
*   this can be downloaded, copied and/or modified in any way you see fit.
*   Please be aware that all public code samples provided by Nutanix are unofficial in nature,
*   are provided as examples only, are unsupported and will need to be heavily scrutinized
*   and potentially modified before they can be used in a production environment.
*   All such code samples are provided on an as-is basis,and Nutanix expressly disclaims all warranties, express or implied.
*   All code samples are © Nutanix, Inc., and are provided as-is under the MIT license.
*   (https://opensource.org/licenses/MIT)


        print("Type 1: Cluster info")
        print("Type 2: Host info")
        print("Type 3: Vm info")
        print("Type 4: Image info")
        print("Type 5: Container info")
        print("Type 6: Network info")
        print("Type 7: Upload new image from URL")
        print("Type 8: Create new VM from disk image with cloud-init")
        print("Type 9: VM Power on/off operation")
        print("Type 10: Delete VM operation")
        print("Type 11: Collect performance data(cpu/mem) for VM or host")
        print("Type 12: Disk detail info")


        print("Type 1: Cluster info")
        print("Type 2: Host info")
        print("Type 3: Vm info")
        print("Type 4: Image info")
        print("Type 5: Container info")
        print("Type 6: Network info")
        print("Type 7: Upload new image from URL")
        print("Type 8: Create new VM from disk image with cloud-init")
        print("Type 9: VM Power on/off operation")
        print("Type 10: Delete VM operation")
        print("Type 11: Collect performance data(cpu/mem) for VM or host")
        print("Type 12: Disk detail info")


1. You can get cluster detail such as ntp,dns,data service IP address

2. You will see all hostnames  and their uuid first then if you provide uuid, will get host detail for the host

3. All VM list will be shown with their name,uuid,power status, will get VM detail if you provide uuid 

4. All image list will be shown with their name,uuid, vm_disk_id, will get image detail if you provide uuid 

5. All container list will be shown with their name,uuid, will get container detail if you provide uuid 

6. All network list will be shown with their name,uuid, will get network detail if you provide uuid 

7.Upload image from URL only for now - require container uuid to upload

8. You can create new VM from disk image from image service with cloud-init config file
   cloud-init file needs to be located in the same folder with nxcli file

9. You can transit VM power status by providing VM uuid

10. You can delete VM by providing VM uuid (cvm won't be deleted by this call but don't try in production)

11. You can collect performance data - cpu/mem for the host or vm max 4 hr historical data, min 30 sec polling period.

12. All disk list will be listed with detail info.

