#!/bin/bash
date
echo 'Fetching data from mgh-props'
python getdata.py
cp refsearch.html ./templates/NEW-de-templates/refsearch.html
cp distinctlocations.html ./templates/NEW-de-templates/distinctlocations.html
cat ./templates/NEW-de-templates/distinctlocations.html
echo 'Data fetched'
echo 'NEW ENGLISH NEW-de'
python ./scripts/NEW-de-scripts/topsix.py
echo 'topsix NEW-de fin'
python ./scripts/NEW-de-scripts/latest.py
echo 'latest NEW-de fin'
python ./scripts/NEW-de-scripts/proplist.py
echo 'proplist NEW-de fin'
python ./scripts/NEW-de-scripts/propdetail.py
echo 'propdetail NEW-de fin'
date
echo 'finished'