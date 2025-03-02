#!/usr/bin/sh

apt update
apt install ffmpeg -y

python3 -m pip install -r requirements.txt