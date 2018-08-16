FROM ubuntu:latest
MAINTAINER gac55@cam.ac.uk

# Noninteractive mode for mailutils setup
ENV DEBIAN_FRONTEND="noninteractive"

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/hello-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/hello-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

#Install Cron
RUN apt-get update
RUN apt-get -y install cron 
RUN apt-get -y install python-pip python-dev build-essential 
RUN apt-get install -y git
RUN apt-get install -y nano
RUN apt-get install -y mailutils
RUN echo "postfix postfix/mailname string gmail.com" | debconf-set-selections
RUN echo "postfix postfix/main_mailer_type string 'Internet Site'" | debconf-set-selections
RUN apt-get install -y ssmtp

# Python dependencies
RUN pip install awscli
RUN pip install ujson
RUN pip install requests
RUN pip install Slacker
RUN pip install python-dateutil
RUN pip install boto
RUN pip install magicdate
RUN pip install filechunkio

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log

WORKDIR /home

# Get the repo
COPY . .

RUN python dir_gen.py

# Setup repo directories
RUN bin/tfl_build

# AWS S3 credential setup
RUN cat mail > /etc/ssmtp/ssmtp.conf
RUN mkdir /root/.aws/
RUN mv config  /root/.aws/
RUN mv credentials  /root/.aws/
ENV AWS_ACCESS_KEY_ID="TODO"
ENV AWS_SECRET_ACCESS_KEY="TODO"
ENV HOME=/root