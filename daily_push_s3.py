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

print "Daily push to AWS S3 storage"
# we are bundling the previous days data.

yesterday = magicdate.magicdate('yesterday')

# Connect to S3

conn = boto.connect_s3(host="s3-eu-west-1.amazonaws.com")
print "Connected to S3"

# Bucket name

bucket_name = "londonrealtimefeeds"

# Look up bucket, to see if exists 
bucket = conn.lookup(bucket_name)

# If it doesn't, create it 

if not bucket:
	print "Bucket doesn't exist, creating bucket: "
	conn.create_bucket(bucket_name, location=Location.EU)
	message = "First time S3 setup. Bucket created " + str(bucket_name)
	print message
else:
	print "Bucket", bucket_name , "exists. Adding data to it."

# Connect to the bucket itself

print "connecting to bucket"
b = conn.get_bucket(bucket_name)

# Find location of data locally

dir_file = gzip.open("/home/TfL_feeds/directory_data.json.gz")
dir_json = json.load(dir_file)

# Define folder name within local directory
file_name = dir_json['home_directory'] + "/data/" + str(yesterday) + ".tar.gz"
message = "working on folder for: " + str(file_name)
print message

file_exists = os.path.isfile(file_name)

if file_exists == True:
	
	# Upload variables
	upload_chunk_size = 52428800
	file_size = os.stat(file_name).st_size

	# Checksum 
	
	# Setup a multi part upload request
	mp = b.initiate_multipart_upload(os.path.basename(file_name))
	
	# Break data up into sections for sending
	chunk_count = int(math.ceil(file_size / float(upload_chunk_size)))
	
	# Iterate through sections and fire them off
	print "Beginning upload"
	
	for i in range(chunk_count):
		offset = upload_chunk_size * i
		bytes = min(upload_chunk_size, file_size - offset)
		with FileChunkIO(file_name, 'r', offset=offset,bytes=bytes) as fp:
			mp.upload_part_from_file(fp, part_num=i + 1)
	
	mp.complete_upload()
	print "Upload complete"
