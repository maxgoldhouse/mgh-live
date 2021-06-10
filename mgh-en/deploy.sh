#!/bin/bash
date
echo 'Fetching data from mgh-props'
python getdata.py
cp refsearch.html ./templates/NEW-nl-templates/refsearch.html
cp distinctlocations.html ./templates/NEW-nl-templates/distinctlocations.html
cat ./templates/NEW-nl-templates/distinctlocations.html
echo 'Data fetched'
echo 'NEW ENGLISH NEW-nl'
python ./scripts/NEW-nl-scripts/topsix.py
echo 'topsix NEW-nl fin'
python ./scripts/NEW-nl-scripts/latest.py
echo 'latest NEW-nl fin'
python ./scripts/NEW-nl-scripts/proplist.py
echo 'proplist NEW-nl fin'
python ./scripts/NEW-nl-scripts/propdetail.py
echo 'propdetail NEW-nl fin'
date
echo 'finished'