#!/usr/bin/python
# -*- coding: utf-8 -*-
import jinja2
import os
import sqlite3
import _all_rubrunsdata
import _mghsettings
import _mgh_data
import sys
reload(sys);
sys.setdefaultencoding("utf8")

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

#templateLoader = jinja2.FileSystemLoader(_mghsettings.EN_TEMPLATEFOLDER)
#templateEnv = jinja2.Environment( loader=templateLoader )
#TEMPLATE_FILE = "proplist.jinja"

#template = templateEnv.get_template( TEMPLATE_FILE )

thetopsix = _mgh_data.proplists['topsix']
for fetchprop in thetopsix:
	row = _mgh_data.props[str(fetchprop)]
	print row['ref']

print "++++++++++++++++++++++++++++++++++++++++++++++++++++++"

for eachprop in _mgh_data.proplists['9-10']:
	row = _mgh_data.props[str(eachprop)]
	print row['ref'], row['price'], row['pid']
'''
for rubrun in _all_rubrunsdata.rubruns:

	for propinlist in _mgh_data.proplists[rubrun['rubrun']]:# LIMIT 20
		thisprop = _mgh_data.props[str(propinlist)]
		propurl = '/'+str(thisprop['beds'])+'-bed-'+thisprop['ptype'].replace(' ','-')+'-in-'+thisprop['location'].replace(' ','-')+'-'+thisprop['pid']+'.html'
		if thisprop['rental'] == "True":
		  saleorrent = 'rent'
		else:
		  saleorrent = 'sale'
		print propurl +" "+saleorrent

		'''
