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
                    [--fetch] [--print] [--search] [--options] [--version]

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
  --fetch
  --print
  --search
  --options
  --version
```

Examples
--------

Fetch VMware HCL JSON file:

```
 ./jellyfish.py --fetch
100% [..........................................................................] 2846368 / 2846368%
```

Search for all Dell QLE2462 entries:

```
./jellyfish.py --search --vendor Dell --model QLE2462
{
 "id": "33793",
 "vendor": "Dell EMC",
 "model": "XtremSF 700GB PCIe card",
 "vid": "1344",
 "did": "5150",
 "ssid": "2204",
 "svid": "1344",
 "url": "http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=io&productid=33793",
 "releases": [
  "ESXi 7.0 U3",
  "ESXi 7.0 U2",
  "ESXi 7.0 U1",
  "ESXi 7.0",
  "ESXi 6.7 U3",
  "ESXi 6.7 U2",
  "ESXi 6.7 U1",
  "ESXi 6.7",
  "ESXi 6.5 U3",
  "ESXi 6.5 U2",
  "ESXi 6.5 U1",
  "ESXi 6.5",
  "ESXi 6.0 U3",
  "ESXi 6.0 U2",
  "ESXi 6.0 U1",
  "ESXi 6.0"
 ]
}
{
 "id": "33793",
 "vendor": "Dell EMC",
 "model": "XtremSF 700GB PCIe card",
 "vid": "1344",
 "did": "5150",
 "ssid": "2204",
 "svid": "1344",
 "url": "http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=io&productid=33793",
 "releases": [
  "ESXi 7.0 U3",
  "ESXi 7.0 U2",
  "ESXi 7.0 U1",
  "ESXi 7.0",
  "ESXi 6.7 U3",
  "ESXi 6.7 U2",
  "ESXi 6.7 U1",
  "ESXi 6.7",
  "ESXi 6.5 U3",
  "ESXi 6.5 U2",
  "ESXi 6.5 U1",
  "ESXi 6.5",
  "ESXi 6.0 U3",
  "ESXi 6.0 U2",
  "ESXi 6.0 U1",
  "ESXi 6.0"
 ]
}
```

Search for all Dell QLE2462 entries with the string EMC:

```
./jellyfish.py --search --vendor Dell --model QLE2462 --string EMC
{
 "id": "33793",
 "vendor": "Dell EMC",
 "model": "XtremSF 700GB PCIe card",
 "vid": "1344",
 "did": "5150",
 "ssid": "2204",
 "svid": "1344",
 "url": "http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=io&productid=33793",
 "releases": [
  "ESXi 7.0 U3",
  "ESXi 7.0 U2",
  "ESXi 7.0 U1",
  "ESXi 7.0",
  "ESXi 6.7 U3",
  "ESXi 6.7 U2",
  "ESXi 6.7 U1",
  "ESXi 6.7",
  "ESXi 6.5 U3",
  "ESXi 6.5 U2",
  "ESXi 6.5 U1",
  "ESXi 6.5",
  "ESXi 6.0 U3",
  "ESXi 6.0 U2",
  "ESXi 6.0 U1",
  "ESXi 6.0"
 ]
}
```

Search for all Dell QLE2462 entries with the string EMC and return just the URL:

```
./jellyfish.py --search --vendor Dell --model QLE2462 --string EMC --get url
http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=io&productid=4024
```
