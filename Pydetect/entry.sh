#!/usr/bin/env bash

python3 -m pip install --no-cache-dir -r requirements.txt
python3 main.py

apt update
apt install zip -y

zip solveme.zip encoder.pyc flag
mv solveme.zip ./webroot/solveme.zip

cd webroot
python3 -m http.server 80
