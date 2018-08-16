#!/usr/bin/python
import urllib
import datetime
import time
import gzip
import json

try:
	dir_file = gzip.open("/home/TfL_feeds/directory_data.json.gz")
	dir_json = json.load(dir_file)
	time_stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H')
	time_folder = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')

	# Weekly resolution
	# UK wide GTFS call

	file_name = dir_json['home_directory'] + "/data/" + str(time_folder) + "/UK_gtfs_" + time_stamp + ".zip"

	url = "http://www.gbrail.info/gtfs.zip"

	urllib.urlretrieve(url,file_name)

	message = "Weekly pull of UK wide GTFS complete"
	print message
	
except Exception as e:
	
	message = "general error with api_weekly.py - " + str(e)
	
	print message
