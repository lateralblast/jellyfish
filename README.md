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
- pygments
- json
- bs4
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
usage: jellyfish.py [-h] [--id ID] [--get GET] [--url URL] [--vid VID] [--did DID] [--file FILE] [--ssid SSID]
                    [--svid SVID] [--model MODEL] [--vendor VENDOR] [--hclurl HCLURL] [--string STRING]
                    [--release RELEASE] [--workdir WORKDIR] [--driverurl DRIVERURL] [--mask] [--fetch] [--print]
                    [--search] [--options] [--version] [--driverinfo]

options:
  -h, --help            show this help message and exit
  --id ID
  --get GET
  --url URL
  --vid VID
  --did DID
  --file FILE
  --ssid SSID
  --svid SVID
  --model MODEL
  --vendor VENDOR
  --hclurl HCLURL
  --string STRING
  --release RELEASE
  --workdir WORKDIR
  --driverurl DRIVERURL
  --mask
  --fetch
  --print
  --search
  --options
  --version
  --driverinfo
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

Fetch and process information for specific component ID to extract JSON:

```
./jellyfish.py --driverinfo --driverurl "http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=io&productid=4024"
[
 {
  "CertDetail_Id": 6791600,
  "Release_Id": 485,
  "Component_Id": 4024,
  "DriverName": "qlnativefc",
  "Version": "3.1.8.0-5vmw",
  "Driver_Url": "",
  "DeviceType": "FC",
  "Type": 0,
  "ReleaseVersion": "ESXi 6.7 U3",
  "ReleaseVersionOrig": "ESXi 6.7 U3",
  "inbox_async": "VMware Inbox",
  "Footnotes": null,
  "DeviceDrivers": "qlnativefc  version  3.1.8.0-5vmw",
  "KB_Ids": null,
  "KB_Id": null,
  "KB": "",
  "OS_Use": "Standard",
  "VMwareSupportDate": "February 26, 2015",
  "Major": 6,
  "Minor": 7,
  "Patch": null,
  "Solution": "N/A",
  "FirmwareVersion": "N/A",
  "AddlFirmwareVersion": null,
  "VioSolution": null,
  "SwitchName": null,
  "SwitchFirmwareVersion": null,
  "SwitchBrandName": null,
  "SortOrder": 1300673,
  "Component_Release_Id": 1051398,
  "Configuration_Id": 101,
  "VmklinuxOrNativeDriver": "native"
 },
 {
  "CertDetail_Id": 6232883,
  "Release_Id": 428,
  "Component_Id": 4024,
  "DriverName": "qlnativefc",
  "Version": "3.1.8.0-4vmw",
  "Driver_Url": "",
  "DeviceType": "FC",
  "Type": 0,
  "ReleaseVersion": "ESXi 6.7 U2",
  "ReleaseVersionOrig": "ESXi 6.7 U2",
  "inbox_async": "VMware Inbox",
  "Footnotes": null,
  "DeviceDrivers": "qlnativefc  version  3.1.8.0-4vmw",
  "KB_Ids": null,
  "KB_Id": null,
  "KB": "",
  "OS_Use": "Standard",
  "VMwareSupportDate": "February 26, 2015",
  "Major": 6,
  "Minor": 7,
  "Patch": null,
  "Solution": "N/A",
  "FirmwareVersion": "N/A",
  "AddlFirmwareVersion": null,
  "VioSolution": null,
  "SwitchName": null,
  "SwitchFirmwareVersion": null,
  "SwitchBrandName": null,
  "SortOrder": 1300672,
  "Component_Release_Id": 1020906,
  "Configuration_Id": 101,
  "VmklinuxOrNativeDriver": "native"
 },
 {
  "CertDetail_Id": 5965148,
  "Release_Id": 427,
  "Component_Id": 4024,
  "DriverName": "qlnativefc",
  "Version": "3.0.1.0-5vmw",
  "Driver_Url": "",
  "DeviceType": "FC",
  "Type": 0,
  "ReleaseVersion": "ESXi 6.7 U1",
  "ReleaseVersionOrig": "ESXi 6.7 U1",
  "inbox_async": "VMware Inbox",
  "Footnotes": null,
  "DeviceDrivers": "qlnativefc  version  3.0.1.0-5vmw",
  "KB_Ids": null,
  "KB_Id": null,
  "KB": "",
  "OS_Use": "Standard",
  "VMwareSupportDate": "February 26, 2015",
  "Major": 6,
  "Minor": 7,
  "Patch": null,
  "Solution": "N/A",
  "FirmwareVersion": "N/A",
  "AddlFirmwareVersion": null,
  "VioSolution": null,
  "SwitchName": null,
  "SwitchFirmwareVersion": null,
  "SwitchBrandName": null,
  "SortOrder": 1300671,
  "Component_Release_Id": 1002498,
  "Configuration_Id": 101,
  "VmklinuxOrNativeDriver": "native"
 },
 {
  "CertDetail_Id": 5615912,
  "Release_Id": 369,
  "Component_Id": 4024,
  "DriverName": "qlnativefc",
  "Version": "3.0.1.0-5vmw",
  "Driver_Url": "",
  "DeviceType": "FC",
  "Type": 0,
  "ReleaseVersion": "ESXi 6.7",
  "ReleaseVersionOrig": "ESXi 6.7",
  "inbox_async": "VMware Inbox",
  "Footnotes": null,
  "DeviceDrivers": "qlnativefc  version  3.0.1.0-5vmw",
  "KB_Ids": null,
  "KB_Id": null,
  "KB": "",
  "OS_Use": "Standard",
  "VMwareSupportDate": "February 26, 2015",
  "Major": 6,
  "Minor": 7,
  "Patch": null,
  "Solution": "N/A",
  "FirmwareVersion": "N/A",
  "AddlFirmwareVersion": null,
  "VioSolution": null,
  "SwitchName": null,
  "SwitchFirmwareVersion": null,
  "SwitchBrandName": null,
  "SortOrder": 1300670,
  "Component_Release_Id": 973704,
  "Configuration_Id": 101,
  "VmklinuxOrNativeDriver": "native"
 },
 {
  "CertDetail_Id": 6382436,
  "Release_Id": 429,
  "Component_Id": 4024,
  "DriverName": "qlnativefc",
  "Version": "2.1.50.0-1vmw",
  "Driver_Url": "",
  "DeviceType": "FC",
  "Type": 0,
  "ReleaseVersion": "ESXi 6.5 U3",
  "ReleaseVersionOrig": "ESXi 6.5 U3",
  "inbox_async": "VMware Inbox",
  "Footnotes": null,
  "DeviceDrivers": "qlnativefc  version  2.1.50.0-1vmw",
  "KB_Ids": null,
  "KB_Id": null,
  "KB": "",
  "OS_Use": "Standard",
  "VMwareSupportDate": "February 26, 2015",
  "Major": 6,
  "Minor": 5,
  "Patch": null,
  "Solution": "N/A",
  "FirmwareVersion": "N/A",
  "AddlFirmwareVersion": null,
  "VioSolution": null,
  "SwitchName": null,
  "SwitchFirmwareVersion": null,
  "SwitchBrandName": null,
  "SortOrder": 1300652,
  "Component_Release_Id": 1029023,
  "Configuration_Id": 101,
  "VmklinuxOrNativeDriver": "native"
 },
 {
  "CertDetail_Id": 5537946,
  "Release_Id": 408,
  "Component_Id": 4024,
  "DriverName": "qlnativefc",
  "Version": "2.1.50.0-1vmw",
  "Driver_Url": "",
  "DeviceType": "FC",
  "Type": 0,
  "ReleaseVersion": "ESXi 6.5 U2",
  "ReleaseVersionOrig": "ESXi 6.5 U2",
  "inbox_async": "VMware Inbox",
  "Footnotes": null,
  "DeviceDrivers": "qlnativefc  version  2.1.50.0-1vmw",
  "KB_Ids": null,
  "KB_Id": null,
  "KB": "",
  "OS_Use": "Standard",
  "VMwareSupportDate": "February 26, 2015",
  "Major": 6,
  "Minor": 5,
  "Patch": null,
  "Solution": "N/A",
  "FirmwareVersion": "N/A",
  "AddlFirmwareVersion": null,
  "VioSolution": null,
  "SwitchName": null,
  "SwitchFirmwareVersion": null,
  "SwitchBrandName": null,
  "SortOrder": 1300651,
  "Component_Release_Id": 982757,
  "Configuration_Id": 101,
  "VmklinuxOrNativeDriver": "native"
 },
 {
  "CertDetail_Id": 5179525,
  "Release_Id": 367,
  "Component_Id": 4024,
  "DriverName": "qlnativefc",
  "Version": "2.1.50.0-1vmw",
  "Driver_Url": "",
  "DeviceType": "FC",
  "Type": 0,
  "ReleaseVersion": "ESXi 6.5 U1",
  "ReleaseVersionOrig": "ESXi 6.5 U1",
  "inbox_async": "VMware Inbox",
  "Footnotes": null,
  "DeviceDrivers": "qlnativefc  version  2.1.50.0-1vmw",
  "KB_Ids": null,
  "KB_Id": null,
  "KB": "",
  "OS_Use": "Standard",
  "VMwareSupportDate": "February 26, 2015",
  "Major": 6,
  "Minor": 5,
  "Patch": null,
  "Solution": "N/A",
  "FirmwareVersion": "N/A",
  "AddlFirmwareVersion": null,
  "VioSolution": null,
  "SwitchName": null,
  "SwitchFirmwareVersion": null,
  "SwitchBrandName": null,
  "SortOrder": 1300650,
  "Component_Release_Id": 957498,
  "Configuration_Id": 101,
  "VmklinuxOrNativeDriver": "native"
 },
 {
  "CertDetail_Id": 4854716,
  "Release_Id": 338,
  "Component_Id": 4024,
  "DriverName": "qlnativefc",
  "Version": "2.1.50.0-1vmw",
  "Driver_Url": "",
  "DeviceType": "FC",
  "Type": 0,
  "ReleaseVersion": "ESXi 6.5",
  "ReleaseVersionOrig": "ESXi 6.5",
  "inbox_async": "VMware Inbox",
  "Footnotes": null,
  "DeviceDrivers": "qlnativefc  version  2.1.50.0-1vmw",
  "KB_Ids": null,
  "KB_Id": null,
  "KB": "",
  "OS_Use": "Standard",
  "VMwareSupportDate": "February 26, 2015",
  "Major": 6,
  "Minor": 5,
  "Patch": null,
  "Solution": "N/A",
  "FirmwareVersion": "N/A",
  "AddlFirmwareVersion": null,
  "VioSolution": null,
  "SwitchName": null,
  "SwitchFirmwareVersion": null,
  "SwitchBrandName": null,
  "SortOrder": 1300649,
  "Component_Release_Id": 933564,
  "Configuration_Id": 101,
  "VmklinuxOrNativeDriver": "native"
 },
 {
  "CertDetail_Id": 4980051,
  "Release_Id": 276,
  "Component_Id": 4024,
  "DriverName": "qlnativefc",
  "Version": "2.1.50.0-1vmw",
  "Driver_Url": null,
  "DeviceType": "FC",
  "Type": 0,
  "ReleaseVersion": "ESXi 6.0 U3",
  "ReleaseVersionOrig": "ESXi 6.0 U3",
  "inbox_async": "VMware Inbox",
  "Footnotes": null,
  "DeviceDrivers": "qlnativefc  version  2.1.50.0-1vmw",
  "KB_Ids": null,
  "KB_Id": null,
  "KB": "",
  "OS_Use": "Standard",
  "VMwareSupportDate": "February 26, 2015",
  "Major": 6,
  "Minor": 0,
  "Patch": null,
  "Solution": "N/A",
  "FirmwareVersion": "N/A",
  "AddlFirmwareVersion": null,
  "VioSolution": null,
  "SwitchName": null,
  "SwitchFirmwareVersion": null,
  "SwitchBrandName": null,
  "SortOrder": 1300604,
  "Component_Release_Id": 943063,
  "Configuration_Id": 101,
  "VmklinuxOrNativeDriver": "native"
 },
 {
  "CertDetail_Id": 4581473,
  "Release_Id": 275,
  "Component_Id": 4024,
  "DriverName": "qlnativefc",
  "Version": "2.0.12.0-5vmw",
  "Driver_Url": null,
  "DeviceType": "FC",
  "Type": 0,
  "ReleaseVersion": "ESXi 6.0 U2",
  "ReleaseVersionOrig": "ESXi 6.0 U2",
  "inbox_async": "VMware Inbox",
  "Footnotes": null,
  "DeviceDrivers": "qlnativefc  version  2.0.12.0-5vmw",
  "KB_Ids": null,
  "KB_Id": null,
  "KB": "",
  "OS_Use": "Standard",
  "VMwareSupportDate": "February 26, 2015",
  "Major": 6,
  "Minor": 0,
  "Patch": null,
  "Solution": "N/A",
  "FirmwareVersion": "N/A",
  "AddlFirmwareVersion": null,
  "VioSolution": null,
  "SwitchName": null,
  "SwitchFirmwareVersion": null,
  "SwitchBrandName": null,
  "SortOrder": 1300603,
  "Component_Release_Id": 913431,
  "Configuration_Id": 101,
  "VmklinuxOrNativeDriver": "native"
 },
 {
  "CertDetail_Id": 4375014,
  "Release_Id": 274,
  "Component_Id": 4024,
  "DriverName": "qlnativefc",
  "Version": "2.0.12.0-5vmw",
  "Driver_Url": null,
  "DeviceType": "FC",
  "Type": 0,
  "ReleaseVersion": "ESXi 6.0 U1",
  "ReleaseVersionOrig": "ESXi 6.0 U1",
  "inbox_async": "VMware Inbox",
  "Footnotes": null,
  "DeviceDrivers": "qlnativefc  version  2.0.12.0-5vmw",
  "KB_Ids": null,
  "KB_Id": null,
  "KB": "",
  "OS_Use": "Standard",
  "VMwareSupportDate": "February 26, 2015",
  "Major": 6,
  "Minor": 0,
  "Patch": null,
  "Solution": "N/A",
  "FirmwareVersion": "N/A",
  "AddlFirmwareVersion": null,
  "VioSolution": null,
  "SwitchName": null,
  "SwitchFirmwareVersion": null,
  "SwitchBrandName": null,
  "SortOrder": 1300602,
  "Component_Release_Id": 900184,
  "Configuration_Id": 101,
  "VmklinuxOrNativeDriver": "native"
 },
 {
  "CertDetail_Id": 4375015,
  "Release_Id": 274,
  "Component_Id": 4024,
  "DriverName": "qlnativefc",
  "Version": "2.0.12.0-5vmw",
  "Driver_Url": null,
  "DeviceType": "FC",
  "Type": 0,
  "ReleaseVersion": "ESXi 6.0 U1",
  "ReleaseVersionOrig": "ESXi 6.0 U1",
  "inbox_async": "VMware Inbox",
  "Footnotes": null,
  "DeviceDrivers": "qlnativefc  version  2.0.12.0-5vmw",
  "KB_Ids": null,
  "KB_Id": null,
  "KB": "",
  "OS_Use": "Standard",
  "VMwareSupportDate": "February 26, 2015",
  "Major": 6,
  "Minor": 0,
  "Patch": null,
  "Solution": "N/A",
  "FirmwareVersion": "N/A",
  "AddlFirmwareVersion": null,
  "VioSolution": null,
  "SwitchName": null,
  "SwitchFirmwareVersion": null,
  "SwitchBrandName": null,
  "SortOrder": 1300602,
  "Component_Release_Id": 900184,
  "Configuration_Id": 101,
  "VmklinuxOrNativeDriver": "native"
 },
 {
  "CertDetail_Id": 4202907,
  "Release_Id": 273,
  "Component_Id": 4024,
  "DriverName": "qlnativefc",
  "Version": "2.0.12.0-5vmw",
  "Driver_Url": "",
  "DeviceType": "FC",
  "Type": 1,
  "ReleaseVersion": "ESXi 6.0",
  "ReleaseVersionOrig": "ESXi 6.0",
  "inbox_async": "VMware Async",
  "Footnotes": null,
  "DeviceDrivers": "qlnativefc  version  2.0.12.0-5vmw",
  "KB_Ids": null,
  "KB_Id": null,
  "KB": "",
  "OS_Use": "Standard",
  "VMwareSupportDate": "February 26, 2015",
  "Major": 6,
  "Minor": 0,
  "Patch": null,
  "Solution": "N/A",
  "FirmwareVersion": "N/A",
  "AddlFirmwareVersion": null,
  "VioSolution": null,
  "SwitchName": null,
  "SwitchFirmwareVersion": null,
  "SwitchBrandName": null,
  "SortOrder": 1300601,
  "Component_Release_Id": 883580,
  "Configuration_Id": 101,
  "VmklinuxOrNativeDriver": "native"
 }
]
```

Get data for a key only for the previous example:

```
./jellyfish.py --driverinfo --driverurl "http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=io&productid=4024" --get DriverName
DriverName: "qlnativefc"
```
