#!/usr/bin/sh

python3 main.py
python3 padder.py

ffmpeg -i base_pad.wav -i tones_pad.wav -filter_complex "[0:a]volume=1.0[a0];[1:a]volume=0.1[a1];[a0][a1]amix=inputs=2" -ac 1 ./webroot/transmission.wav


cd webroot/
python3 -m http.server 80