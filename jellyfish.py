#!/usr/bin/env python3

# Name:         jellyfish
# Version:      0.2.0
# Release:      1
# License:      CC BY-NC-SA (Creative Commons Attribution-NonCommercial-ShareAlike)
#               https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode
# Group:        System
# Source:       N/A
# URL:          http://lateralblast.com.au/
# Distribution: UNIX
# Vendor:       Lateral Blast
# Packager:     Richard Spindler <richard@lateralblast.com.au>
# Description:  Python script to process the VMware HCL JSON file produced here:
#               https://www.virten.net/2017/01/vmware-io-devices-hcl-in-json-format/

"""Search the VMware I/O device HCL JSON file and fetch driver details."""

import argparse
import json
import os
import re
import sys

SCRIPT_PATH = os.path.abspath(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)

DEFAULT_HCL_URL = "http://www.virten.net/repo/vmware-iohcl.json"
DRIVER_URL_TEMPLATE = (
    "http://www.vmware.com/resources/compatibility/detail.php"
    "?deviceCategory=io&productid=%s"
)

# Import name: pip package name
REQUIRED_MODULES = {
    "wget": "wget",
    "selenium": "selenium",
    "pygments": "pygments",
}

# Keys in an HCL record that can be searched on
HCL_KEYS = ["id", "vendor", "model", "vid", "did", "ssid", "svid", "url", "releases"]

# Keys in a driver detail record
DRIVER_KEYS = [
    "CertDetail_Id", "Release_Id", "Component_Id", "DriverName", "Version",
    "Driver_Url", "DeviceType", "Type", "ReleaseVersion", "ReleaseVersionOrig",
    "inbox_async", "Footnotes", "DeviceDrivers", "KB_Ids", "KB_Id", "KB",
    "OS_Use", "VMwareSupportDate", "Major", "Minor", "Patch", "Solution",
    "FirmwareVersion", "AddlFirmwareVersion", "VioSolution", "SwitchName",
    "SwitchFirmwareVersion", "SwitchBrandName", "SortOrder",
    "Component_Release_Id", "Configuration_Id", "VmklinuxOrNativeDriver",
]


def install_missing_modules():
    """Install any missing required modules with pip, or exit if that fails."""
    import importlib
    import importlib.util
    import site
    import subprocess

    def find_missing():
        return [
            package for module, package in REQUIRED_MODULES.items()
            if importlib.util.find_spec(module) is None
        ]

    missing = find_missing()
    if not missing:
        return
    print("Installing missing modules: %s" % " ".join(missing))
    command = [sys.executable, "-m", "pip", "install"]
    if sys.prefix != sys.base_prefix:
        attempts = [[]]
    else:
        attempts = [["--user"], ["--user", "--break-system-packages"]]
    for extra in attempts:
        if subprocess.call(command + extra + missing) == 0:
            break
    importlib.invalidate_caches()
    if site.ENABLE_USER_SITE is not False:
        site.addsitedir(site.getusersitepackages())
    missing = find_missing()
    if missing:
        print("Warning:\tUnable to install: %s" % " ".join(missing))
        print("Install manually, e.g.: %s -m pip install %s"
              % (sys.executable, " ".join(missing)))
        sys.exit(1)


def build_parser():
    """Create the command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Process the VMware HCL JSON file and driver information")
    parser.add_argument("--id", help="ID to search for")
    parser.add_argument("--get", help="Get a specific key")
    parser.add_argument("--url", help="URL to search for")
    parser.add_argument("--vid", help="VID to search for")
    parser.add_argument("--did", help="DID to search for")
    parser.add_argument("--file", help="JSON file to read in")
    parser.add_argument("--ssid", help="SSID to search for")
    parser.add_argument("--svid", help="SVID to search for")
    parser.add_argument("--model", help="Model to search for")
    parser.add_argument("--vendor", help="Vendor to search for")
    parser.add_argument("--hclurl", help="URL to fetch the HCL JSON file from")
    parser.add_argument("--string", help="A string to search for")
    parser.add_argument("--release", help="Release to search for")
    parser.add_argument("--workdir", help="Work directory")
    parser.add_argument("--driverurl", help="VMware Driver URL")
    parser.add_argument("--certdetailid", help="VMware Driver Cert Detail ID")
    parser.add_argument("--componentid", help="VMware Driver Component ID")
    parser.add_argument("--releaseid", help="VMware Driver Release ID")
    parser.add_argument("--drivername", help="VMware Driver Name")
    parser.add_argument("--driverversion", help="VMware Driver Version")
    parser.add_argument("--drivertype", help="VMware Driver Type")
    parser.add_argument("--mask", action="store_true",
                        help="Mask MAC addresses etc")
    parser.add_argument("--fetch", action="store_true",
                        help="Fetch VMware HCL file from URL")
    parser.add_argument("--print", action="store_true", help="Print JSON")
    parser.add_argument("--search", action="store_true", help="Search JSON")
    parser.add_argument("--options", action="store_true",
                        help="Display options information")
    parser.add_argument("--version", action="store_true",
                        help="Display version information")
    parser.add_argument("--driverinfo", action="store_true",
                        help="Display driver information")
    return parser


def print_version():
    """Print the version from this script's header comment."""
    with open(SCRIPT_PATH) as script_file:
        for line in script_file:
            match = re.match(r"^# Version:\s*(\S+)", line)
            if match:
                print(match.group(1))
                return


def print_options(parser):
    """Print each option and its help text."""
    print("\nOptions:\n")
    for action in parser._actions:
        if action.option_strings and action.help:
            print("%-16s%s" % (action.option_strings[-1], action.help))
    print("\n")


def handle_output(options, output):
    """Print output, masking sensitive values if --mask was given."""
    if options["mask"]:
        if re.search(r"serial|address|host|id", output.lower()) and ":" in output:
            output = "%s: XXXXXXXX" % output.split(":")[0]
    print(output)


def word_pattern(string):
    """Return a regex matching string as a whole word."""
    return r"\b(?=\w)" + re.escape(string) + r"\b(?!\w)"


def field_matches(value, string):
    """Check if a record value (None, scalar or list) contains string."""
    if value is None:
        return False
    if not isinstance(value, list):
        value = [value]
    pattern = word_pattern(string)
    return any(re.search(pattern, str(entry)) for entry in value)


def print_highlighted(json_text):
    """Print JSON text with terminal syntax highlighting."""
    from pygments import highlight
    from pygments.formatters.terminal256 import Terminal256Formatter
    from pygments.lexers.web import JsonLexer
    print(highlight(json_text, lexer=JsonLexer(), formatter=Terminal256Formatter()))


def load_json(options):
    """Load the ioDevices list from the HCL JSON file into options['data']."""
    with open(options["file"], "r") as json_file:
        options["data"] = json.load(json_file)["data"]["ioDevices"]
    return options


def print_json(options):
    """Print the whole HCL data set as JSON."""
    options = load_json(options)
    print(json.dumps(options["data"], indent=1))


def search_string(options):
    """Search every record for --string, optionally printing one key."""
    key = options["get"]
    pattern = word_pattern(options["string"]) if options["string"] else None
    records = []
    for record in options["data"]:
        if not pattern or not re.search(pattern, str(record)):
            continue
        if key:
            if key not in record:
                continue
            output = json.dumps(record[key], indent=1)
        else:
            output = json.dumps(record, indent=1)
        if output not in records:
            records.append(output)
    for output in records:
        if key and not re.search(r"^[A-Z]", key):
            print("%s: %s" % (key, output))
        else:
            print_highlighted(output)


def search_keys(options):
    """Narrow records by each HCL key given, then print the matches."""
    records = options["data"]
    for hcl_key in HCL_KEYS:
        if not options[hcl_key]:
            continue
        matches = []
        for record in records:
            if not field_matches(record.get(hcl_key), options[hcl_key]):
                continue
            if options["string"] and not re.search(
                    word_pattern(options["string"]), str(record)):
                continue
            matches.append(record)
        records = matches
    key = options["get"]
    for record in records:
        if key and not re.search(r"^[A-Z]", key):
            if key in record:
                print(record[key])
            continue
        print_highlighted(json.dumps(record, indent=1))
        if options["driverinfo"]:
            options["driverurl"] = DRIVER_URL_TEMPLATE % record["id"]
            get_driver_info(options)


def search_json(options):
    """Search the HCL data by key or by string."""
    options = load_json(options)
    if any(options[hcl_key] for hcl_key in HCL_KEYS):
        search_keys(options)
    else:
        search_string(options)


def start_web_driver():
    """Start a headless Firefox web driver."""
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    firefox_options = Options()
    firefox_options.add_argument("-headless")
    return webdriver.Firefox(options=firefox_options)


def fetch_driver_html(options, html_file):
    """Fetch the driver page HTML and save it to html_file."""
    driver = start_web_driver()
    try:
        driver.get(options["driverurl"])
        html_data = driver.page_source
    finally:
        driver.quit()
    with open(html_file, "w") as open_file:
        open_file.write(html_data)


def extract_driver_json(html_file, json_file):
    """Extract the driver details JSON from html_file into json_file."""
    with open(html_file, "r") as open_file:
        html_data = open_file.readlines()
    for html_line in html_data:
        if "Component_Id" in html_line and "var details =" in html_line:
            html_line = html_line.split("var details =")[1].strip()
            html_line = re.sub(r";$", "", html_line)
            with open(json_file, "w") as open_file:
                open_file.write(html_line)
            return True
    return False


def get_driver_info(options):
    """Print driver details for options['driverurl'], caching in the workdir."""
    if "productid" not in options["driverurl"]:
        handle_output(options, "Warning:\tInvalid URL")
        return
    prod_id = options["driverurl"].split("=")[-1]
    html_file = os.path.join(options["workdir"], "%s.html" % prod_id)
    json_file = os.path.join(options["workdir"], "%s.json" % prod_id)
    if not os.path.exists(json_file):
        if not os.path.exists(html_file):
            fetch_driver_html(options, html_file)
        if not extract_driver_json(html_file, json_file):
            os.remove(html_file)
            handle_output(
                options, "Warning:\tNo driver details found for %s" % prod_id)
            return
    with open(json_file, "r") as open_file:
        json_data = json.load(open_file)
    key = options["get"]
    if not key:
        print_highlighted(json.dumps(json_data, indent=1))
        return
    outputs = []
    for record in json_data:
        if key not in record:
            continue
        output = json.dumps(record[key])
        if output not in outputs:
            print("%s: %s" % (key, output))
        outputs.append(output)


def fetch_hcl(options):
    """Download the HCL JSON file, keeping any existing file on failure."""
    import wget
    temp_file = "%s.tmp" % options["file"]
    try:
        wget.download(options["hclurl"], temp_file)
        os.replace(temp_file, options["file"])
    except Exception as error:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        handle_output(options, "Warning:\tFailed to fetch %s: %s"
                      % (options["hclurl"], error))


def main():
    """Parse arguments and run the requested action."""
    parser = build_parser()
    if len(sys.argv) == 1:
        parser.print_help()
        return 0
    options = vars(parser.parse_args())
    if options["version"]:
        print_version()
        return 0
    if options["options"]:
        print_options(parser)
        return 0

    install_missing_modules()

    # --release is stored under the HCL key name
    options["releases"] = options["release"]
    options["workdir"] = options["workdir"] or SCRIPT_DIR
    options["file"] = options["file"] or os.path.join(
        SCRIPT_DIR, "vmware-iohcl.json")
    options["hclurl"] = options["hclurl"] or DEFAULT_HCL_URL

    if options["fetch"]:
        fetch_hcl(options)
    if not os.path.exists(options["file"]):
        handle_output(
            options, "Warning:\tJSON file %s not found" % options["file"])
        return 1
    if options["print"]:
        print_json(options)
    elif options["driverinfo"] and options["driverurl"]:
        get_driver_info(options)
    elif options["search"]:
        search_json(options)
    return 0


if __name__ == "__main__":
    sys.exit(main())
