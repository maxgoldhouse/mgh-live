#!/bin/bash
switch="$1"
sudo pip install Jinja2
echo 'Fetching data from mgh-props'
python getdata.py
cp refsearch.html ./templates/de-templates/refsearch.html
cp refsearch.html ./templates/en-templates/refsearch.html
cp refsearch.html ./templates/fr-templates/refsearch.html
cp refsearch.html ./templates/nl-templates/refsearch.html
substring=EN
if [ "$switch" != "${switch%$substring*}" ] ||  [ -z "$switch" ]
then
echo 'ENGLISH'
python ./scripts/en-scripts/kyerofeed.py
echo 'kyrofeed fin'
python ./scripts/en-scripts/topsix.py
echo 'topsix EN fin'
python ./scripts/en-scripts/latest.py
echo 'latest EN fin'
python ./scripts/en-scripts/proplist.py
echo 'proplist EN fin'
python ./scripts/en-scripts/propdetail.py
echo 'propdetail EN fin'
fi
substring=DE
if [ "$switch" != "${switch%$substring*}" ] ||  [ -z "$switch" ]
then
echo 'DEUTSCH'
python ./scripts/de-scripts/de_topsix.py
echo 'topsix DE fin'
python ./scripts/de-scripts/de_latest.py
echo 'latest DE fin'
python ./scripts/de-scripts/de_proplist.py
echo 'proplist DE fin'
python ./scripts/de-scripts/de_propdetail.py
echo 'propdetail DE fin'
fi
substring=FR
if [ "$switch" != "${switch%$substring*}" ] ||  [ -z "$switch" ]
then
echo 'FRANCAIS'
python ./scripts/fr-scripts/fr_topsix.py
echo 'topsix FR fin'
python ./scripts/fr-scripts/fr_latest.py
echo 'latest FR fin'
python ./scripts/fr-scripts/fr_proplist.py
echo 'proplist FR fin'
python ./scripts/fr-scripts/fr_propdetail.py
echo 'propdetail FR fin'
fi
substring=NL
if [ "$switch" != "${switch%$substring*}" ] ||  [ -z "$switch" ]
then
echo 'NEDERLANDS'
python ./scripts/nl-scripts/nl_topsix.py
echo 'topsix NL fin'
python ./scripts/nl-scripts/nl_latest.py
echo 'latest NL fin'
python ./scripts/nl-scripts/nl_proplist.py
echo 'proplist NL fin'
python ./scripts/nl-scripts/nl_propdetail.py
echo 'propdetail NL fin'
python ./scripts/iv-nl-scripts/iv_nl_topsix.py
echo 'topsix IV fin'
python ./scripts/iv-nl-scripts/iv_nl_proplist.py
echo 'proplist IV fin'
python ./scripts/iv-nl-scripts/iv_nl_propdetail.py
echo 'propdetail IV fin'
fi
substring=EN
if [ "$switch" != "${switch%$substring*}" ] ||  [ -z "$switch" ]
then
echo 'EN deploy'
cd ~/src/mgh-live/deploy/EN
gcloud app deploy app.yaml --version 1 --project www-mgh-3 --quiet
fi
substring=DE
if [ "$switch" != "${switch%$substring*}" ] ||  [ -z "$switch" ]
then
echo 'DE deploy'
cd ~/src/mgh-live/deploy/DE
gcloud app deploy app.yaml --version 1 --project www-mgh-3-de --quiet
fi
substring=FR
if [ "$switch" != "${switch%$substring*}" ] ||  [ -z "$switch" ]
then
echo 'FR deploy'
cd ~/src/mgh-live/deploy/FR
gcloud app deploy app.yaml --version 1 --project www-mgh-3-fr --quiet
fi
substring=NL
if [ "$switch" != "${switch%$substring*}" ] ||  [ -z "$switch" ]
then
echo 'NL deploy'
cd ~/src/mgh-live/deploy/NL
gcloud app deploy app.yaml --version 1 --project www-mgh-3-nl --quiet
fi
cd ~/src/mgh-live
git clean -f -d -q
echo 'git cleaned up'
sudo pip uninstall Jinja2 --yes
