![alt tag](https://raw.githubusercontent.com/lateralblast/jellyfish/master/jellyfish.jpg)

JELLYFISH
=========

Jellyfish is a script to process the VMware HCL JSON file produced here:

https://www.virten.net/2017/01/vmware-io-devices-hcl-in-json-format/

Requirements
------------

Required Python modules:

- subprocess
- argparse
- json
- sys
- os
- re

License
-------

This software is licensed as CC-BA (Creative Commons By Attrbution)

http://creativecommons.org/licenses/by/4.0/legalcode

Usage
-----

```
./jellyfish.py --help
usage: jellyfish.py [-h] [--file FILE] [--get GET] [--id ID] [--url URL] [--vid VID] [--did DID] [--ssid SSID]
                    [--svid SVID] [--model MODEL] [--vendor VENDOR] [--release RELEASE] [--string STRING] [--mask]
                    [--print] [--search] [--options] [--version]

options:
  -h, --help         show this help message and exit
  --file FILE
  --get GET
  --id ID
  --url URL
  --vid VID
  --did DID
  --ssid SSID
  --svid SVID
  --model MODEL
  --vendor VENDOR
  --release RELEASE
  --string STRING
  --mask
  --print
  --search
  --options
  --version
```

Examples
--------

Search for all Dell QLE2462 entries:

```
./jellyfish.py --search --vendor Dell --model QLE2462
{'id': '4063', 'vendor': 'Dell Inc.', 'model': 'QLogic QLE2462', 'vid': '1077', 'did': '2432', 'ssid': '0138', 'svid': '1077', 'url': 'http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=io&productid=4063', 'releases': ['ESXi 6.7 U3', 'ESXi 6.7 U2', 'ESXi 6.7 U1', 'ESXi 6.7', 'ESXi 6.5 U3', 'ESXi 6.5 U2', 'ESXi 6.5 U1', 'ESXi 6.5', 'ESXi 6.0 U3', 'ESXi 6.0 U2', 'ESXi 6.0 U1', 'ESXi 6.0']}
{'id': '4024', 'vendor': 'Dell EMC', 'model': 'Qlogic QLE2462-E-SP', 'vid': '1077', 'did': '2432', 'ssid': '0138', 'svid': '1077', 'url': 'http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=io&productid=4024', 'releases': ['ESXi 6.7 U3', 'ESXi 6.7 U2', 'ESXi 6.7 U1', 'ESXi 6.7', 'ESXi 6.5 U3', 'ESXi 6.5 U2', 'ESXi 6.5 U1', 'ESXi 6.5', 'ESXi 6.0 U3', 'ESXi 6.0 U2', 'ESXi 6.0 U1', 'ESXi 6.0']}
```

Search for all Dell QLE2462 entries with the string EMC:

```
./jellyfish.py --search --vendor Dell --model QLE2462 --string EMC
{'id': '4024', 'vendor': 'Dell EMC', 'model': 'Qlogic QLE2462-E-SP', 'vid': '1077', 'did': '2432', 'ssid': '0138', 'svid': '1077', 'url': 'http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=io&productid=4024', 'releases': ['ESXi 6.7 U3', 'ESXi 6.7 U2', 'ESXi 6.7 U1', 'ESXi 6.7', 'ESXi 6.5 U3', 'ESXi 6.5 U2', 'ESXi 6.5 U1', 'ESXi 6.5', 'ESXi 6.0 U3', 'ESXi 6.0 U2', 'ESXi 6.0 U1', 'ESXi 6.0']}
```
