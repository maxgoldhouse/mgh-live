#!/bin/bash
date
echo 'mgh-en deploy.sh Fetching data from mgh-props'
python getdata.py
cp refsearch.html ./templates/NEW-en-templates/refsearch.html
cp distinctlocations.html ./templates/NEW-en-templates/distinctlocations.html
echo 'Data fetched'
echo 'NEW FRENCH'
python ./scripts/NEW-fr-scripts/topsix.py
echo 'mgh-en deploy.sh topsix NEW-EN fin'
python ./scripts/NEW-fr-scripts/latest.py
echo 'mgh-en deploy.sh latest NEW-EN fin'
python ./scripts/NEW-fr-scripts/proplist.py
echo 'mgh-en deploy.sh proplist NEW-EN fin'
python ./scripts/NEW-fr-scripts/propdetail.py
echo 'mgh-en deploy.sh propdetail NEW-EN fin'
date
echo 'finished'