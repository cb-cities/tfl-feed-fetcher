#!/usr/bin/python
import master_api_call
import time

daily_resolution = 60*60*24 / 60 / 24

# 1 minute resolution
api_dict_60 = [
	{"url" : "https://api.tfl.gov.uk/line/mode/bus/status",
	"resolution" : 60 
	},
	{"url" : "https://api.tfl.gov.uk/line/mode/national-rail/status" ,
	"resolution" : 60
	},
	{"url" : "https://api.tfl.gov.uk/Occupancy/CarPark" ,
	"resolution" : 60
	},
	{"url" : "https://api.tfl.gov.uk/line/mode/tube,overground,dlr,tflrail/status",
	"resolution" : 60
	},
	{"url" : "https://api.tfl.gov.uk/line/mode/tube/status",
	"resolution" : 60
	}
]

for i in range(0,daily_resolution):
	if i == daily_resolution-1:
		last_call = True
	else:
		last_call = False
	master_api_call.api_sender(api_dict_60,last_call)