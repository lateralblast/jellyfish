#!/usr/bin/env python

# Name:         jellyfish
# Version:      0.0.7
# Release:      1
# License:      CC-BA (Creative Commons By Attrbution)
#               http://creativecommons.org/licenses/by/4.0/legalcode
# Group:        System
# Source:       N/A
# URL:          http://lateralblast.com.au/
# Distribution: UNIX
# Vendor:       Lateral Blast
# Packager:     Richard Spindler <richard@lateralblast.com.au>
# Description:  Python script to process the VMware HCL JSON file produced here:
#               https://www.virten.net/2017/01/vmware-io-devices-hcl-in-json-format/

# Import modules

import subprocess
import argparse
import json
import sys
import os
import re


# Set some defaults

script_exe = sys.argv[0]
script_dir = os.path.dirname(script_exe)

# Check we have pip installed

try:
  from pip._internal import main
except ImportError:
  os.system("easy_install pip")
  os.system("pip install --upgrade pip")

# install and import a python module

def install_and_import(package):
  import importlib
  try:
    importlib.import_module(package)
  except ImportError:
    command = "python3 -m pip install --user %s" % (package)
    os.system(command)
  finally:
    globals()[package] = importlib.import_module(package)

# load wget

try:
  import wget
except ImportError:
  install_and_import("wget")
  import wget

# Load selenium

try:
  from selenium import webdriver
except ImportError:
  install_and_import("selenium")
  from selenium import webdriver

# Load bs4

try:
  from bs4 import BeautifulSoup
except ImportError:
  install_and_import("bs4")
  from bs4 import BeautifulSoup

# Load pygments

try:
  from pygments import highlight
except ImportError:
  install_and_import("pygments")
  from pygments import highlight

from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.web import JsonLexer  

# Print version

def print_version(script_exe):
  file_array = file_to_array(script_exe)
  version    = list(filter(lambda x: re.search(r"^# Version", x), file_array))[0].split(":")[1]
  version    = re.sub(r"\s+", "", version)
  print(version)

# Print help

def print_help(script_exe):
  print("\n")
  command  = "%s -h" % (script_exe)
  os.system(command)
  print("\n")

# Read a file into an array

def file_to_array(file_name):
  file_data  = open(file_name)
  file_array = file_data.readlines()
  return file_array

# Print options

def print_options(script_exe):
  file_array = file_to_array(script_exe)
  opts_array = list(filter(lambda x:re.search(r"add_argument", x), file_array))
  print("\nOptions:\n")
  for line in opts_array:
    line = line.rstrip()
    if re.search(r"#", line):
      option = line.split('"')[1]
      info   = line.split("# ")[1]
      if len(option) < 8:
        string = "%s\t\t\t%s" % (option,info)
      else:
        if len(option) < 16:
          string = "%s\t\t%s" % (option,info)
        else:
          string = "%s\t%s" % (option,info)
      print(string)
  print("\n")

# Handle output

def handle_output(options, output):
  if options['mask'] == True:
    if re.search(r"serial|address|host|id", output.lower()):
      if re.search(":", output):
        param  = output.split(":")[0]
        output = "%s: XXXXXXXX" % (param)
  print(output)
  return

# Execute command

def execute_command(options, command):
  process = subprocess.Popen(command, shell=True, stdout = subprocess.PIPE, )
  output  = process.communicate()[0].decode()
  if options['verbose'] == True:
    string = "Output:\n%s" % (output)
    handle_output(options, string)

# Load JSON

def load_json(options):
  with open(options['file'], 'r') as json_file:
    json_data = json.load(json_file)
    json_data = json_data['data']
    json_data = json_data['ioDevices']
    options['data'] = json_data
    return(options)

# Print JSON

def print_json(options):
  options = load_json(options)
  output  = json.dumps(options['data'], indent=1)
  print(output)

# Search JSON

def search_json(options):
  options = load_json(options)
  found   = False
  records = []
  for item in options['keys']:
    if options[item]:
      found = True
  if found == False:
    for record in options['data']:
      if options['string']:
        patern = r"\b(?=\w)" + re.escape(options['string']) + r"\b(?!\w)"
        if re.search(patern, str(record)):
          if options["get"]:
            item   = options['get']
            output = record[item]
            output = json.dumps(output, indent=1)
          else:
            output = json.dumps(record, indent=1)
          if not output in records:
            records.append(output)
    for record in records:
      json_data = record
      output = highlight(
        json_data,
        lexer=JsonLexer(),
        formatter=Terminal256Formatter(),
      )
      print(output)
    return
  records = options['data']
  for item in options['keys']:
    if options[item]:
      outputs = []
      for record in records:
        patern = r"\b(?=\w)" + re.escape(options[item]) + r"\b(?!\w)"
        if re.search(patern, record[item]):
          if options['string']:
            patern = r"\b(?=\w)" + re.escape(options['string']) + r"\b(?!\w)"
            if re.search(patern, str(record)):
              outputs.append(record)
          else:
            outputs.append(record)
      records = {}
      records = outputs
  for output in records:
    if options['get']:
      item = options['get']
      print(output[item])
    else:
      json_data = json.dumps(record, indent=1)
      output = highlight(
        json_data,
        lexer=JsonLexer(),
        formatter=Terminal256Formatter(),
      )
      print(output)
  return

# Initiate web client

def start_web_driver():
  from selenium.webdriver.firefox.options import Options
  options = Options()
  options.headless = True
  driver = webdriver.Firefox(options=options)
  return driver

# Get driver information from VMware URL

def get_driver_info(options):
  if not re.search(r"productid", options['driverurl']):
    handle_output(options,"Warning:\tInvalid URL")
    return
  prod_id   = re.split("=", options['driverurl'])[-1]
  html_file = "%s/%s.html" % (options['workdir'], prod_id)
  json_file = "%s/%s.json" % (options['workdir'], prod_id)
  if not os.path.exists(json_file):
    if not os.path.exists(html_file):
      driver = start_web_driver()
      driver.get(options['driverurl'])
      html_data = driver.page_source
      open_file = open(html_file, "w")
      open_file.write(html_data)
      open_file.close()
    open_file = open(html_file, "r")
    html_data = open_file.readlines()
    open_file.close()
    for html_line in html_data:
      if re.search(r"Component_Id", html_line):
        html_line = html_line.split("var details =")[1]
        html_line = re.sub(r"\;$", "", html_line)
        open_file = open(json_file, "w")
        open_file.write(html_line)
        open_file.close()
  open_file = open(json_file, "r")
  json_data = open_file.read()
  open_file.close()
  json_data = json.loads(json_data)
  if options['get']:
    item = options['get']
    for record in json_data:
      record = json.loads(record[item])
      print(record[item])
  else:
    json_data = json.dumps(json_data, indent=1)
    output = highlight(
      json_data,
      lexer=JsonLexer(),
      formatter=Terminal256Formatter(),
    )
  print(output)
  return

# If we have no command line arguments print help

if sys.argv[-1] == sys.argv[0]:
  print_help(script_exe)
  exit()

# Get command line arguments

parser = argparse.ArgumentParser()
parser.add_argument("--id", required=False)               # ID to search for
parser.add_argument("--get", required=False)              # Get a specific key
parser.add_argument("--url", required=False)              # URL to search for
parser.add_argument("--vid", required=False)              # VID to search for
parser.add_argument("--did", required=False)              # VID to search for
parser.add_argument("--file", required=False)             # JSON file to read in
parser.add_argument("--ssid", required=False)             # SSID to search for
parser.add_argument("--svid", required=False)             # SVID to search for
parser.add_argument("--model", required=False)            # Model to search for
parser.add_argument("--vendor", required=False)           # Vendor to search for
parser.add_argument("--hclurl", required=False)           # Vendor to search for
parser.add_argument("--string", required=False)           # A string to search for
parser.add_argument("--release", required=False)          # Vendor to search for
parser.add_argument("--workdir", required=False)          # Work directory
parser.add_argument("--driverurl", required=False)        # VMware Driver URL 
parser.add_argument("--certdetailid", required=False)     # VMware Driver Cert Detail ID 
parser.add_argument("--componentid", required=False)      # VMware Driver Component ID 
parser.add_argument("--releaseid", required=False)        # VMware Driver Release ID 
parser.add_argument("--drivername", required=False)       # VMware Driver Name
parser.add_argument("--driverversion", required=False)    # VMware Driver Version
parser.add_argument("--drivertype", required=False)       # VMware Driver Type
parser.add_argument("--mask", action='store_true')        # Mask MAC addresses etc
parser.add_argument("--fetch", action='store_true')       # Fetch VMware HCL file from URL
parser.add_argument("--print", action='store_true')       # Print JSON
parser.add_argument("--search", action='store_true')      # Search JSON
parser.add_argument("--options", action='store_true')     # Display options information
parser.add_argument("--version", action='store_true')     # Display version information
parser.add_argument("--driverinfo", action='store_true')  # Display driver information

options = vars(parser.parse_args())

# Handle release flag

if options['release']:
  options['releases'] = options['release']
else:
  options['releases'] = None

# Create a list of keys

options['keys'] = [ 'id', 'vendor', 'model', 'vid', 'did', 'ssid', 'svid', 'url', 'releases' ]

# Handle version switch

if options['version']:
  script_exe = sys.argv[0]
  print_version(script_exe)
  exit()

# Handle options switch

if options['options']:
  script_exe = sys.argv[0]
  print_options(script_exe)
  exit()

# Handle workdir switch

if not options['workdir']:
  options['workdir'] = script_dir

# Handle file switch

if not options['file']:
  options['file'] = "%s/vmware-iohcl.json" % (script_dir)

# Handle hclurl switch:

if not options['hclurl']:
  options['hclurl'] = "http://www.virten.net/repo/vmware-iohcl.json"

# Handle fetch switch

if options['fetch']:
  if os.path.exists(options['file']):
    os.remove(options['file'])
  wget.download(options['hclurl'],options['file'])

# Exit if not JSON file

if not os.path.exists(options['file']):
  string = "Warning:\tJSON file %s not found" % (options['file'])
  handle_output(options, string)
  exit()

# Handle print flag

if options['print']:
  print_json(options)
  exit()

# Handle driverinfo flag

if options['driverinfo']:
  if options['driverurl']:
    get_driver_info(options)
    exit()

# Handle search flag

if options['search']:
  search_json(options)
  exit()

