#!/bin/bash


# apt-get update && apt-get install -y python3-pip

# Run the Python script
python3 -m pip install requirements.txt
python3 /usr/local/bin/script.py

# Start Apache server
httpd-foreground