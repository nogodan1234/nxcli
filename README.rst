nxcli: Nutanix API client for devops
#############################################

This readme file is specifically for the **nxcli** Python code sample.

The setup instructions are the same as all other python code samples in this repository.  This file is provided as additional/supplemental information for this specific code sample.

Please see the `main <https://github.com/nutanixdev/code-samples/tree/master/python>`_ page for general instructions.

**Usage instructions are shown at the bottom of this page.**

Code Sample Details
...................

A quick intro, first.  The **nxcli** program can be used for simple nutanix cluster operation with Python 3.  The expectation is that users wanting to do nutanix cluster operation without Prism UI access.  For example:

- Get various entity information - cluster,host,vm,image,network,disks,task etc
- Upload image from URL 
- Create single or multiple VM(s) from disk image with cloud-init 
- Power on/off all VMs at once(CVMs won't be affected)
- Delete VM
- Collect host,vm performance data from arithmos service

**nxcli** has been provided for devopslish operation something similar awscli or azurecli against nutanix prism element cluster:

#- A single batch should not contain no more than 60 individual requests
#- Additional exception handling should be added before using this in production

Usage
-----

It is strongly recommended to be careful when you do VM delete operation or power-off operation to prevent undesired outcome in production

.. code-block:: bash

   usage: ./nxcli

.. code-block:: bash
   if this was the first time executed, it will ask for cluster detail:
   or it will use saved cluster configuration to communicate 

Example:

.. code-block:: bash
   this requires to have "nxapilib.py" file in same directory as a method library
   python3 and various optional python pkgs are required to install prior to execute

.. code-block:: bash