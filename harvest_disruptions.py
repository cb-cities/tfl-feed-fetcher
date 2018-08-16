import requests
import time
from pprint import pprint
import json
import datetime
import gzip
import os.path
import dateutil
import commands
from dateutil.relativedelta import *
from dateutil.parser import *
from datetime import *

now = parse(commands.getoutput("date"))
start_date = now.date()
end_date = start_date + relativedelta(months=1)

url = "https://api.tfl.gov.uk/Road/All/Disruption?startDate="+str(start_date) + "&endDate=" + str(end_date)

response = requests.get(url)
results = response.json()
response = str(response)

if response != "<Response [200]>":
	message = "API error on url: " + str(url)
	print message

file_name = str(start_date) + '_disruptions.json.gz'

# New day scenario - new file
if os.path.isfile(file_name) == False:
	print "new file created for: ", str(start_date)
	with gzip.open(file_name, 'w') as outfile:
		json.dump(results, outfile, indent =2)
	message = "TfL road disruptions feed update. " + str(len(results)) + " new updates for period: " + str(start_date) +" to " + str(end_date)
	print message

# Old day scenario - need to check if individual warning already exists and update accordingly
else:
	print "File exists for: ", str(start_date)
	old_results_f = gzip.open(file_name)
	old_results = json.load(old_results_f)
	new_updates = []
	for old_result in old_results:
		exists = False
		for result in results:
			if old_result != result:
				exists = False
			if old_result != result:
				exists = True
		if exists == False:
			new_updates.append(result)
	if len(new_updates) == 0:
		print "No updates made to file"
	else:
		print "File updated with " + str(len(new_updates)) + " new road disruptions updates today"
		message = "TfL disruptions feed update. " + str(len(new_updates)) + " new road disruption warnings today"
		print message
	old_results.append(new_updates)
	with gzip.open(file_name, 'w') as outfile:
		json.dump(old_results, outfile, indent =2)
		