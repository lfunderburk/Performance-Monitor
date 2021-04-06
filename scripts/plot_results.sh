#!/bin/bash

TIME1=`date +%Y-%m-%d_%H-%M-%S`

echo "Current working directory: `pwd`"
echo "Starting run at: " ${TIME1}


# ---------------------------------------------------------------------

echo "Begin Script"
echo " "

cd /home/lauragf/Dropbox/RC/Performance_Monitor/

source Environments/perfenv/bin/activate

# run the following once 
#pip install -r requirements.txt

echo "HI"

echo "Current working directory: `pwd`"

/home/lauragf/anaconda3/bin/python3.8 /home/lauragf/Dropbox/RC/Performance_Monitor/plot_performance.py "./logs/" "intensity"

/home/lauragf/anaconda3/bin/python3.8 /home/lauragf/Dropbox/RC/Performance_Monitor/plot_performance.py "./test_dir/" "berlin"

deactivate

for x in *.html;do 
mv "$x" ./Performance-Monitor/
done

cd ./Performance-Monitor

git  pull origin main

for x in *.html;do
git add "$x"
done

git commit -m ${TIME1}" performance test result"

git push origin main

echo "End Script"

