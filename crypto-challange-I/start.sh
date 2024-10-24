#!/bin/bash

# Update package list and install python3-venv if not already installed
apt-get update && apt-get install -y python3-venv

# Create a virtual environment
python3 -m venv /usr/local/bin/venv

# Activate the virtual environment
source /usr/local/bin/venv/bin/activate

# Install required packages
pip install -r /usr/local/bin/requirements.txt

# Run the Python script
python /usr/local/bin/script.py

# Start Apache server
httpd-foreground