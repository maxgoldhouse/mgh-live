#!/bin/bash
date
echo 'Fetching data from mgh-props'
python getdata.py
cp refsearch.html ./templates/NEW-en-templates/refsearch.html
cp distinctlocations.html ./templates/NEW-en-templates/distinctlocations.html
cat ./templates/NEW-en-templates/distinctlocations.html
echo 'Data fetched'
echo 'NEW ENGLISH NEW-en'
python ./scripts/NEW-en-scripts/topsix.py
echo 'topsix NEW-en fin'
python ./scripts/NEW-en-scripts/latest.py
echo 'latest NEW-en fin'
python ./scripts/NEW-en-scripts/proplist.py
echo 'proplist NEW-en fin'
python ./scripts/NEW-en-scripts/propdetail.py
echo 'propdetail NEW-en fin'
date
echo 'finished'