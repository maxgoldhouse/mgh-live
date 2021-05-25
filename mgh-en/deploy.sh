#!/bin/bash
date
echo 'mgh-en deploy.sh Fetching data from mgh-props'
python getdata.py
cp refsearch.html ./templates/NEW-en-templates/refsearch.html
cp distinctlocations.html ./templates/NEW-en-templates/distinctlocations.html
cat ./templates/NEW-en-templates/distinctlocations.html
echo 'Data fetched'
echo 'NEW ENGLISH NEW-en'
python ./scripts/NEW-en-scripts/topsix.py
echo 'mgh-en deploy.sh topsix NEW-en fin'
python ./scripts/NEW-en-scripts/latest.py
echo 'mgh-en deploy.sh latest NEW-en fin'
python ./scripts/NEW-en-scripts/proplist.py
echo 'mgh-en deploy.sh proplist NEW-en fin'
python ./scripts/NEW-en-scripts/propdetail.py
echo 'mgh-en deploy.sh propdetail NEW-en fin'
date
echo 'finished'