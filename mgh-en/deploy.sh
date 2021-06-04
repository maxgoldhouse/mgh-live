#!/bin/bash
date
echo 'mgh-en deploy.sh Fetching data from mgh-props'
python getdata.py
cp refsearch.html ./templates/NEW-nl-templates/refsearch.html
cp distinctlocations.html ./templates/NEW-nl-templates/distinctlocations.html
cat ./templates/NEW-nl-templates/distinctlocations.html
echo 'Data fetched'
echo 'NEW ENGLISH NEW-nl'
python ./scripts/NEW-nl-scripts/topsix.py
echo 'mgh-en deploy.sh topsix NEW-nl fin'
python ./scripts/NEW-nl-scripts/latest.py
echo 'mgh-en deploy.sh latest NEW-nl fin'
python ./scripts/NEW-nl-scripts/proplist.py
echo 'mgh-en deploy.sh proplist NEW-nl fin'
python ./scripts/NEW-nl-scripts/propdetail.py
echo 'mgh-en deploy.sh propdetail NEW-nl fin'
date
echo 'finished'