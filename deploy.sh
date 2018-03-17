#!/bin/bash
#
pip install -r requirements.txt
python getdata.py
cat refsearch.html
cp refsearch.html ./templates/de-templates/refsearch.html
cp refsearch.html ./templates/en-templates/refsearch.html
cp refsearch.html ./templates/fr-templates/refsearch.html
cp refsearch.html ./templates/nl-templates/refsearch.html
python ./scripts/en-scripts/kyerofeed.py
python ./scripts/en-scripts/topsix.py
python ./scripts/en-scripts/latest.py
python ./scripts/en-scripts/proplist.py
python ./scripts/en-scripts/propdetail.py
python ./scripts/de-scripts/de_topsix.py
python ./scripts/de-scripts/de_latest.py
python ./scripts/de-scripts/de_proplist.py
python ./scripts/de-scripts/de_propdetail.py
python ./scripts/fr-scripts/fr_topsix.py
python ./scripts/fr-scripts/fr_latest.py
python ./scripts/fr-scripts/fr_proplist.py
python ./scripts/fr-scripts/fr_propdetail.py
python ./scripts/nl-scripts/nl_topsix.py
python ./scripts/nl-scripts/nl_latest.py
python ./scripts/nl-scripts/nl_proplist.py
python ./scripts/nl-scripts/nl_propdetail.py
python ./scripts/iv-nl-scripts/iv_nl_topsix.py
python ./scripts/iv-nl-scripts/iv_nl_proplist.py
python ./scripts/iv-nl-scripts/iv_nl_propdetail.py

cd ./deploy/EN
gcloud app deploy app.yaml --version 1 --project www-mgh-3
cd ./deploy/DE
gcloud app deploy app.yaml --version 1 --project www-mgh-3-de
cd ./deploy/FR
gcloud app deploy app.yaml --version 1 --project www-mgh-3-fr
cd ./deploy/NL
gcloud app deploy app.yaml --version 1 --project www-mgh-3-nl
