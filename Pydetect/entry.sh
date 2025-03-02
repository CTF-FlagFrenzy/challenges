#!/usr/bin/env bash

python3 main.py

zip solveme.zip encoder.pyc flag
mv solveme.zip ./webroot/solveme.zip

cd webroot
python3 -m http.server 80
