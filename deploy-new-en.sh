#!/bin/bash
date
echo 'Fetching data from mgh-props'
python getdata.py
echo 'Data fetched'
echo 'NEW ENGLISH'
python -m ./scripts/NEW-en-scripts/topsix.py
echo 'NEW topsix EN fin'
#python ./scripts/NEW-en-scripts/latest.py
#echo 'NEW latest EN fin'
#python ./scripts/NEW-en-scripts/proplist.py
#echo 'NEW proplist EN fin'
#python scripts/NEW-en-scripts/propdetail.py
#echo 'NEW propdetail EN fin'
date
