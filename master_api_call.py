#!/usr/bin/python
import requests
import time
from pprint import pprint
import json
import datetime
import gzip
import os.path
from dateutil.parser import *
from dateutil.relativedelta import *
import commands
import smtplib
import multiprocessing

message = "API calls beginning"
print message

def api_sender(dict_list,last_call):
	
	# start the clock
	start = time.time()
	print "working on data resolution : "
	
	print(dict_list[0]['resolution'])
	
	# List of api requests
	url_list = []
	for dict_lis in dict_list:
		name = dict_lis['url']
		url_list.append(name)
	
	for api in dict_list:
		# Read dict_list
		index = api['url'].rfind('uk')
		name = api['url'][(index+3):]
		
		# API call
		response = requests.get(api['url'])
		try:
			results = response.json()
			response = str(response)	
			
			# Check the response
			if response != "<Response [200]>":
				message = "API error on url: " + str(url)
				print message
			
			# Time - labels and records
			time_stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H_%M')
			time_folder = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
			time_stamp_readable = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
			
			print "current time: ", str(time_stamp_readable)
			# Directory management
			try:
				dir_file = gzip.open("/home/TfL_feeds/directory_data.json.gz")
			except IOError:
				dir_file = gzip.open("directory_data.json.gz")
			dir_json = json.load(dir_file)
			name_man = time_folder + "/" + name.replace("/","_") + "_"
			file_name = dir_json['home_directory'] + "/data/" + name_man + str(time_stamp) + '.json.gz'
			
			# Results dict
			results_dump = []
			data = {
				"epoch" : time.time(),
				"time_stamp" : time_stamp_readable,
				"updates" : results
				}
			results_dump.append(data)
			
			# Create folder for day if not exists
			if os.path.isdir((dir_json['home_directory'] + "/data/" + time_folder)) == False:
				os.mkdir(dir_json['home_directory'] + "/data/" + time_folder)
				print "Created folder for ", time_folder
				message = "New folder created for " + time_folder
				print message
			
			# Create file if not exists
			if os.path.isfile(file_name) == False:
				print "Writing file: ", file_name
				with gzip.open(file_name, 'w') as outfile:
					json.dump(results_dump, outfile, indent =3)
			
			# Append to existing file if exists
			elif os.path.isfile(file_name) == True:
				print "Adding new responses to existing file: ", file_name
				previous_file = gzip.open(file_name)
				previous_results = json.load(previous_file)
				# Add old results to new results
				bundled_results = previous_results + results_dump
				# Write file again 
				with gzip.open(file_name, 'w') as outfile:
					json.dump(bundled_results, outfile, indent =3)
		except:
			print "No JSON response returned by server. Skipping this time slot."
	
	end = time.time()
	loop_elapsed = end - start
	time_diff = api['resolution'] - loop_elapsed
	# Avoid negative wait times. 
	if time_diff < 0:
		time_diff = 0
	print "Sleeping for ", time_diff , "seconds"
	if last_call == True:
		time.sleep(0)
	else:
		time.sleep(time_diff)
		