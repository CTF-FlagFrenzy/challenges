#!/usr/bin/sh

python3 main.py
python3 -m pysstv --mode Robot36 placed.png ./transmission.wav
ffmpeg -i transmission.wav -filter:a "volume=0.1" ./webroot/transmission.wav

cd webroot/
python3 -m http.server 80