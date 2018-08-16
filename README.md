Overview
========

An extremely hacky python script.

This is an automated server for polling and storing a range of different TfL feeds. These feeds are polled at their defined temporal resolution, stored as an hourly file, within a daily folder. At the end of each day, this local folder is compressed and transferred to `AWS S3` for storage. 

We have four api calls

- 1 minute resolution
	- `https://api.tfl.gov.uk/line/mode/bus/status`
	- `https://api.tfl.gov.uk/line/mode/national-rail/status`
	- `https://api.tfl.gov.uk/Occupancy/CarPark`
	- `https://api.tfl.gov.uk/line/mode/tube,overground,dlr,tflrail/status`
	- `https://api.tfl.gov.uk/line/mode/tube/status`

- 5 minute resolution
	- `https://api.tfl.gov.uk/bikepoint`
	- `https://api.tfl.gov.uk/road`

- 1 hour resolution
	- `https://api.tfl.gov.uk/AirQuality`

- 1 hour resolution
	- `GTFS from TfL feeds` Via [CommuteStream/tflgtfs Repo](https://github.com/CommuteStream/tflgtfs)

- 1 week resolution
	- `UK wide GTFS`

These `API` calls are bundled into a daily folder. At the end of each day, this folder is sent to S3.
		
Scheduling
=====


Each of the different Python scripts are called at midnight at will run at the specified resolution until the end of the day. The `daily_push_s3.py` is called at 1am and this bunldes all of the previous days data and moves it to `S3`. 

This is managed by cron. 

Most API's are called at 10m and run for 24hrs, managed internally in Python. The daily S3 push is called at 11am. 

The `tfl_gtfs` is called by cron every hour:

```
0 10 * * * python /home/TfL_feeds/api_60.py 2>&1 | mail -s "api_60.py ouput" TODO@gmail.com

0 10 * * * python /home/TfL_feeds/api_300.py 2>&1 | mail -s "api_300.py ouput" TODO@gmail.com

0 10 * * * python /home/TfL_feeds/api_3600.py 2>&1 | mail -s "api_3600.py ouput" TODO@gmail.com

0 11 * * * python /home/TfL_feeds/daily_push_s3.py 2>&1 | mail -s "daily_push_s3.py ouput" TODO@gmail.com

0 15 * * 6 python /home/TfL_feeds/api_weekly.py 2>&1 | mail -s "api_weekly.py.py ouput" TODO@gmail.com

0 * * * * python /home/TfL_feeds/tfl_gtfs.py 2>&1 | mail -s "tfl_gtfs.py.py ouput" TODO@gmail.com
```


Usage - Docker
===============

This repo contains a `dockerfile` which will build a docker container and automate the `API` requests with Cron.

The docker image is a modified version of [schicking's rust](https://hub.docker.com/r/schickling/rust/) rust build. 

`docker build -t "your_name/feed_image:latest" path/to/TfL_feeds/`
