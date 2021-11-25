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

