#!/bin/bash
date
echo 'www-mgh-3 deploy.sh Fetching data from mgh-props'
python getdata.py
cp refsearch.html ./templates/NEW-en-templates/refsearch.html
echo 'Data fetched'
echo 'NEW ENGLISH'
python ./scripts/NEW-en-scripts/topsix.py
echo 'mgh-en deploy.sh topsix NEW-EN fin'
python ./scripts/NEW-en-scripts/latest.py
echo 'mgh-en deploy.sh latest NEW-EN fin'
python ./scripts/NEW-en-scripts/proplist.py
echo 'mgh-en deploy.sh proplist NEW-EN fin'
python ./scripts/NEW-en-scripts/propdetail.py
echo 'mgh-en deploy.sh propdetail NEW-EN fin'
date