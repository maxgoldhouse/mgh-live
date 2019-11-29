#!/bin/bash
date
echo 'www-mgh-3-fr deploy.sh Fetching data from mgh-props'
python getdata.py
echo 'Data fetched'
cp refsearch.html ./templates/fr-templates/refsearch.html
echo 'NEW ENGLISH'
python ./scripts/fr-scripts/fr_topsix.py
echo 'www-mgh-3-fr deploy.sh topsix EN fin'
python ./scripts/fr-scripts/fr_latest.py
echo 'www-mgh-3-fr deploy.sh latest EN fin'
python ./scripts/fr-scripts/fr_proplist.py
echo 'www-mgh-3-fr deploy.sh proplist EN fin'
python ./scripts/fr-scripts/fr_propdetail.py
echo 'www-mgh-3-fr deploy.sh propdetail EN fin'
date