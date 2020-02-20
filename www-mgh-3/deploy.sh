#!/bin/bash
date
echo 'www-mgh-3 deploy.sh Fetching data from mgh-props'
python getdata.py
cp refsearch.html ./templates/en-templates/refsearch.html
echo 'Data fetched'
echo 'EN'
python ./scripts/en-scripts/topsix.py
echo 'www-mgh-3 deploy.sh topsix EN fin'
##-#python ./scripts/en-scripts/latest.py
##-#echo 'www-mgh-3 deploy.sh latest EN fin'
python ./scripts/en-scripts/proplist.py
echo 'www-mgh-3 deploy.sh proplist EN fin'
python ./scripts/en-scripts/propdetail.py
echo 'www-mgh-3 deploy.sh propdetail EN fin'
date