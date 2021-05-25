#!/bin/bash
date
echo 'mgh-en deploy.sh Fetching data from mgh-props'
python getdata.py
cp refsearch.html ./templates/NEW-fr-templates/refsearch.html
cp distinctlocations.html ./templates/NEW-fr-templates/distinctlocations.html
cat ./templates/NEW-fr-templates/distinctlocations.html
echo 'Data fetched'
echo 'NEW ENGLISH NEW-fr'
python ./scripts/NEW-fr-scripts/topsix.py
echo 'mgh-en deploy.sh topsix NEW-fr fin'
python ./scripts/NEW-fr-scripts/latest.py
echo 'mgh-en deploy.sh latest NEW-fr fin'
python ./scripts/NEW-fr-scripts/proplist.py
echo 'mgh-en deploy.sh proplist NEW-fr fin'
python ./scripts/NEW-fr-scripts/propdetail.py
echo 'mgh-en deploy.sh propdetail NEW-fr fin'
date
echo 'finished'