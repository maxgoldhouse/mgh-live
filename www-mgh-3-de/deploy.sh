#!/bin/bash
date
echo 'www-mgh-3-de  deploy.sh Fetching data from mgh-props'
python getdata.py
echo 'Data fetched'
echo 'NEW ENGLISH'
python ./scripts/de-scripts/de_topsix.py
echo 'www-mgh-3-de  deploy.sh topsix DE fin'
python ./scripts/de-scripts/de_latest.py
echo 'www-mgh-3-de  deploy.sh latest DE fin'
python ./scripts/de-scripts/de_proplist.py
echo 'www-mgh-3-de  deploy.sh proplist DE fin'
python ./scripts/de-scripts/de_propdetail.py
echo 'www-mgh-3-de deploy.sh propdetail DE fin'
date