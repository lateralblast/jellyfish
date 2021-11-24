#!/usr/bin/env python

# Name:         jellyfish
# Version:      0.0.0
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
  command    = "%s -h" % (script_exe)
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

# If we have no command line arguments print help

if sys.argv[-1] == sys.argv[0]:
  print_help(script_exe)
  exit()

# Get command line arguments

parser = argparse.ArgumentParser()
parser.add_argument("--options", action='store_true')    # Display options information
parser.add_argument("--version", action='store_true')    # Display version information

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




