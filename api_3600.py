#!/usr/bin/python
import master_api_call

daily_resolution = 60*60*24 / 3600 /24

# 1 hour resolution
api_dict_3600 = [
	{"url" : "https://api.tfl.gov.uk/AirQuality",
	"resolution" : 3600
	}
]

for i in range(0,daily_resolution):
	if i == daily_resolution-1:
		last_call = True
	else:
		last_call = False
	master_api_call.api_sender(api_dict_3600,last_call)