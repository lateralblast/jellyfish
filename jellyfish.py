#!/usr/bin/env python

# Name:         jellyfish
# Version:      0.0.1
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

# If we have no command line arguments print help

if sys.argv[-1] == sys.argv[0]:
  print_help(script_exe)
  exit()

# Get command line arguments

parser = argparse.ArgumentParser()
parser.add_argument("--file", required=False)        	 # JSON file to read in
parser.add_argument("--mask", action='store_true')     # Mask MAC addresses etc
parser.add_argument("--print", action='store_true')    # Print JSON
parser.add_argument("--options", action='store_true')  # Display options information
parser.add_argument("--version", action='store_true')  # Display version information

options = vars(parser.parse_args())

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
  with open(options['file'], 'r') as json_file:
    json_data   = json.load(json_file)
    json_output = json.dumps(json_data, indent=1)
    print(json_output)

