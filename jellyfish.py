#!/usr/bin/env python

# Name:         jellyfish
# Version:      0.0.4
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

# Print version

def print_version(script_exe):
  file_array = file_to_array(script_exe)
  version    = list(filter(lambda x: re.search(r"^# Version", x), file_array))[0].split(":")[1]
  version    = re.sub(r"\s+","",version)
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
    if re.search(r"#",line):
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

def handle_output(options,output):
  if options['mask'] == True:
    if re.search(r"serial|address|host|id",output.lower()):
      if re.search(":",output):
        param  = output.split(":")[0]
        output = "%s: XXXXXXXX" % (param)
  print(output)
  return

# Execute command

def execute_command(options,command):
  process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, )
  output  = process.communicate()[0].decode()
  if options['verbose'] == True:
    string = "Output:\n%s" % (output)
    handle_output(options,string)

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
    for output in records:
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
      print(output)
  return

# If we have no command line arguments print help

if sys.argv[-1] == sys.argv[0]:
  print_help(script_exe)
  exit()

# Get command line arguments

parser = argparse.ArgumentParser()
parser.add_argument("--file", required=False)        	 # JSON file to read in
parser.add_argument("--get", required=False)           # Get a specific key
parser.add_argument("--id", required=False)            # ID to search for
parser.add_argument("--url", required=False)           # URL to search for
parser.add_argument("--vid", required=False)           # VID to search for
parser.add_argument("--did", required=False)           # VID to search for
parser.add_argument("--ssid", required=False)          # SSID to search for
parser.add_argument("--svid", required=False)          # SVID to search for
parser.add_argument("--model", required=False)         # Model to search for
parser.add_argument("--vendor", required=False)        # Vendor to search for
parser.add_argument("--release", required=False)       # Vendor to search for
parser.add_argument("--string", required=False)        # A string to search for
parser.add_argument("--mask", action='store_true')     # Mask MAC addresses etc
parser.add_argument("--print", action='store_true')    # Print JSON
parser.add_argument("--search", action='store_true')   # Search JSON
parser.add_argument("--options", action='store_true')  # Display options information
parser.add_argument("--version", action='store_true')  # Display version information

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

# Handle file switch

if not options['file']:
  options['file'] = "%s/vmware-iohcl.json" % (script_dir)

# Exit if not JSON file

if not os.path.exists(options['file']):
  string = "Warning:\tJSON file %s not found" % (options['file'])
  handle_output(options, string)
  exit()

# Handle print flag

if options['print']:
  print_json(options)
  exit()

# Handle search flag

if options['search']:
  search_json(options)
  exit()

