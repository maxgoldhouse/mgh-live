#!/bin/bash
sudo pip3 install Jinja2
date
echo 'mgh-en deploy.sh Fetching data from mgh-props'
#-#python getdata.py
#-#cp refsearch.html ./templates/NEW-en-templates/refsearch.html
#-#cp distinctlocations.html ./templates/NEW-en-templates/distinctlocations.html
echo 'Data fetched'
echo 'NEW ENGLISH'
#-#python ./scripts/NEW-en-scripts/topsix.py
#-#echo 'mgh-en deploy.sh topsix NEW-EN fin'
#-#python ./scripts/NEW-en-scripts/latest.py
#-#echo 'mgh-en deploy.sh latest NEW-EN fin'
#-#python ./scripts/NEW-en-scripts/proplist.py
#-#echo 'mgh-en deploy.sh proplist NEW-EN fin'
python3 ./scripts/NEW-en-scripts/propdetail.py
echo 'mgh-en deploy.sh propdetail NEW-EN fin'
sudo pip uninstall Jinja2 --yes
date