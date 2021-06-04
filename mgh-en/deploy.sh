#!/bin/bash
date
echo 'mgh-en deploy.sh Fetching data from mgh-props'
python getdata.py
cp refsearch.html ./templates/NEW-de-templates/refsearch.html
cp distinctlocations.html ./templates/NEW-de-templates/distinctlocations.html
cat ./templates/NEW-de-templates/distinctlocations.html
echo 'Data fetched'
echo 'NEW ENGLISH NEW-de'
python ./scripts/NEW-de-scripts/topsix.py
echo 'mgh-en deploy.sh topsix NEW-de fin'
python ./scripts/NEW-de-scripts/latest.py
echo 'mgh-en deploy.sh latest NEW-de fin'
python ./scripts/NEW-de-scripts/proplist.py
echo 'mgh-en deploy.sh proplist NEW-de fin'
python ./scripts/NEW-de-scripts/propdetail.py
echo 'mgh-en deploy.sh propdetail NEW-de fin'
date
echo 'finished'