#!/bin/bash

TIME1=`date +%Y-%m-%d_%H-%M-%S`

echo "Current working directory: `pwd`"
echo "Starting run at: " ${TIME1}


# ---------------------------------------------------------------------

echo "Begin Script"
echo " "

cd /home/lauragf/Dropbox/RC/Performance_Monitor/

source Environments/perfenv/bin/activate

#pip install -r requirements.txt

echo "HI"

echo "Current working directory: `pwd`"

/home/lauragf/anaconda3/bin/python3.8 performance_monitor.py

deactivate

echo "End Script"


