#!/usr/bin/python
import gzip
import ujson as json
import time
import os

try:

	# home_dir = expanduser("~")
	home_dir = os.getcwd()
	# home_dir = home_dir + "/Aoife"
	print "Identifying home directory"
	print(home_dir)
	output = {
		"home_directory" : home_dir
	}
	print "Dumping to file for use"

	with gzip.open("./directory_data.json.gz", 'w+') as outfile:
		json.dump(output,outfile,indent=1)

except Exception as e:
	message = "Something has gone wrong! Error message: " + str(e)
	print message