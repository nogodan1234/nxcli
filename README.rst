nxcli: Nutanix API client for devops
#############################################

This readme file is specifically for the **nxcli** program.

The setup instructions are the same as all other python program in this repository.  This file is provided as additional/supplemental program for this specific user purpose.

Please see the `main <https://github.com/nutanixdev/code-samples/tree/master/python>`_ page for general instructions.

**Usage instructions are shown at the bottom of this page.**

Code Sample Details
...................

A quick intro, first.  The **nxcli** program can be used for simple nutanix cluster operation from cli.  The expectation is that users wanting to do nutanix cluster operation without Prism UI access.  For example:

- Get various entity information - cluster,host,vm,image,network,disks,task etc from cli
- Upload image from URL 
- Create single or multiple VM(s) from disk image with cloud-init from cli at once
- Power on/off all VMs at once(CVMs won't be affected)
- Delete VM 
- Collect host,vm performance data from arithmos service

**nxcli** has been provided for devopslish operation something similar awscli or azurecli against nutanix prism element cluster:

- this program requires to have "nxapilib.py" file in same directory as a method library
- python3 and various optional python pkgs are required to install prior to execute, you can check from import sentence in source file - or error msg you get :)

Usage
-----

It is strongly recommended to be careful when you do 10. VM delete operation or 9. Power-off operation to prevent undesired outcome in production

.. code-block:: bash

   usage: ./nxcli

    Be aware you are in $YOUR_CLUSTER_NAME cluster($CLUSTR_VIP) as $CLUSTER_USER user
    What kind of operation do you want?

    #### MENU ####

    Type 0: Check specific task status
    Type 1: Cluster info
    Type 2: Host info
    Type 3: Vm info
    Type 4: Image info
    Type 5: Container info
    Type 6: Network info
    Type 7: Upload new image from URL
    Type 8: Create new VM from disk image with cloud-init(bulk opt)
    Type 9: VM Power on/off operation(bulk opt)
    Type 10: Delete VM operation
    Type 11: Performance data(cpu/mem) for VM or host
    Type 12: Cluster disk detail info
    Type 13: New cluster setup - EULA,Pulse,NTP etc
    Type 14: Run new ncc health checks
    Type 15: Create new managed network(ip pool)
    Type q: Exit program

.. code-block:: bash
   if this was the first time executed, it will ask for cluster detail:
   or it will use saved cluster configuration under your home directory( ~/.nx/config)
   