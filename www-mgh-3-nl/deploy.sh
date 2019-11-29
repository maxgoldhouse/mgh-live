#!/bin/bash
date
echo 'www-mgh-3-nl deploy.sh Fetching data from mgh-props'
python getdata.py
echo 'Data fetched'
cp refsearch.html ./templates/nl-templates/refsearch.html
cp refsearch.html ./templates/iv-nl-templates/refsearch.html
echo 'NL'
python ./scripts/nl-scripts/nl_topsix.py
echo 'www-mgh-3-nl deploy.sh topsix EN fin'
python ./scripts/nl-scripts/nl_latest.py
echo 'www-mgh-3-nl deploy.sh latest EN fin'
python ./scripts/nl-scripts/nl_proplist.py
echo 'www-mgh-3-nl deploy.sh proplist EN fin'
python ./scripts/nl-scripts/nl_propdetail.py
echo 'www-mgh-3-nl deploy.sh propdetail EN fin'
echo 'iv-NL'
python ./scripts/iv-nl-scripts/iv_nl_topsix.py
echo 'www-mgh-3-nl iv deploy.sh topsix EN fin'
python ./scripts/iv-nl-scripts/iv_nl_proplist.py
echo 'www-mgh-3-nl iv deploy.sh proplist EN fin'
python ./scripts/iv_nl_scripts/iv_nl_propdetail.py
echo 'www-mgh-3-nl iv deploy.sh propdetail EN fin'
date