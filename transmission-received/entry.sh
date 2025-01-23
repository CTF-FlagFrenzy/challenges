#/usr/bin/sh

python3 -m pip install -r requirements.txt
python3 main.py
python3 -m pysstv --mode Robot36 placed.png ./webroot/transmission.wav

cd webroot/
python3 -m http.server 80