#!/usr/bin/python
import os
import time
import boto
import boto.s3
from boto.s3.connection import Location
from boto.s3.key import Key
import magicdate
import gzip
import json
import glob
import logging
from filechunkio import FileChunkIO
import math
import shutil
from pprint import pprint
import subprocess

print "Daily file tody up. Pre S3 push"

# we are bundling the previous days data.
yesterday = magicdate.magicdate('yesterday')

dir_file = gzip.open("/home/TfL_feeds/directory_data.json.gz")
dir_json = json.load(dir_file)
os.chdir(dir_json['home_directory'] + "/data/")

# Define folder name within local directory
folder_name = str(yesterday)

message = "Tarring and compressing " + str(folder_name)
print message

folder_exists = os.path.isdir(folder_name)
folder = (folder_name + ".tar.gz")

print "Working on, ", str(folder)

# Tar and compress them
subprocess.call(["tar -zcvf "+ folder + " "+ folder_name + "/"],shell=True)

# clean up - remove files from directory
for file in glob.glob(folder_name+"/*"):
	os.remove(file)
	print "File removed: ", file

# Remove the empty folder
os.rmdir(folder_name)
print folder_name: ", deleted"



