#!/bin/bash
date
echo 'mgh-en deploy.sh Fetching data from mgh-props'
python2 ../getdata.py
cp refsearch.html ./templates/NEW-nl-templates/refsearch.html
cp distinctlocations.html ./templates/NEW-nl-templates/distinctlocations.html
echo 'Data fetched'
echo 'NEW ENGLISH'
python2 ../scripts/NEW-nl-scripts/topsix.py
echo 'mgh-en deploy.sh topsix NEW-nl fin'
python2 ../scripts/NEW-nl-scripts/latest.py
echo 'mgh-en deploy.sh latest NEW-nl fin'
python2 ../scripts/NEW-nl-scripts/proplist.py
echo 'mgh-en deploy.sh proplist NEW-nl fin'
python2 ../scripts/NEW-nl-scripts/propdetail.py
echo 'mgh-en deploy.sh propdetail NEW-nl fin'
date
echo 'finished'