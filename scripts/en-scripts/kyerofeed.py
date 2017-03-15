#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys);
sys.setdefaultencoding("utf8")
sys.path.insert(0, './')
import jinja2
import os
import _all_rubrunsdata
import _mghsettings
import _mgh_data

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

#template setup detail.jinja
templateLoader = jinja2.FileSystemLoader(_mghsettings.EN_TEMPLATEFOLDER)
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "kyero.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

def removeumlauts(text):
	outchars = {u'\xb4':'&acute;',u'\u20ac':'&#x80;',u'\xe1':'a',u'\xf1':'n',u'\xed':'i',u'\u2013':'',u'\xa8':'',u'\xad':'-',u'Ä':'&#xC4;',u'ä':'&#xE4;',u'Ë':'&#xCB;',u'ë':'&#xEB;',u'Ï':'&#xCF;',u'ï':'&#xEF;',u'Ö':'&#xD6;',u'ö':'&#xF6;',u'ß':'&#xDF;',u'Ü':'&#xDC;',u'ü':'&#xFC;','&Aacute;':'&#xC1;','&aacute;':'&#xE1;','&acute;':'a'}
	for i, j in outchars.iteritems():
		text = text.replace(i, j)
	return text


#loop for each property record in the database
propdict = {}
propdict['props'] = []
for eachprop in _mgh_data.proplists['kyero']:
	row = _mgh_data.props[str(eachprop)]
	if row['salestage'] == '0':
		picurldictlist = []
		slidecount = 1
		#for i, pic in enumerate(row['pics']):
		    #row['pics'][i] = pic.replace('s0','s35-p')

		for pic in row['pics']:
		    picurldict = {}
		    picurldict['id'] = slidecount
		    picurldict['img'] = pic.strip().replace('s640','s0')
		    picurldictlist.append(picurldict)
		    slidecount += 1

		#for pic in picurldictlist:
			#print pic['id']
			#print pic['img']

	    #prepare the vars to pass to the template
		pooltype = ['yes', 'private', 'community']
		
		if row['rental'] == 'True':
			saleorrent = 'rent'
		else:
			saleorrent = 'sale'
		if row['pool'].lower() in pooltype:
			pool = '1'
		else:
			pool = '0'
		pagename = row['pid']+'-'+str(row['beds'])+'-bed-'+row['ptype'].replace(' ','-')+'-in-'+row['location'].replace(' ','-')
		propurl = 'https://www.maxgoldhouse.com/'+str(row['beds'])+'-bed-'+row['ptype'].replace(' ','-')+'-in-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
		prop = {}

		prop['propdescription'] = row['description'].replace('&euro;','&#x80;')
		prop['propdescription_DE'] = row['DE'].replace('&euro;','&#x80;')
		prop['propdescription_FR'] = row['FR'].replace('&euro;','&#x80;')
		prop['propdescription_NL'] = row['NL'].replace('&euro;','&#x80;')
		prop['saleorrent'] = saleorrent
		prop['date'] = row['lastedited']
		if row['offplan'] == 'True':
    			prop['frequency'] = 'new_build'
		else:
    			prop['frequency'] = row['frequency']
		prop['beds'] = row['beds']
		prop['baths'] = row['baths']
		prop['livingarea'] = row['living']
		prop['plotsize'] = row['plot']
		prop['pool'] = pool
		prop['propid'] = row['pid']
		prop['propref'] = row['ref'][:12]
		prop['propurl'] = propurl
		prop['town']=row['town']
		prop['locationdetail']=row['location']
		prop['province']=row['province']
		prop['proptype']=row['ptype']
		prop['price'] = row['price']
		prop['images'] = picurldictlist #prop['slide'],prop['src']
		propdict['props'].append(prop)
		outputText = template.render(propdict)
		file = open(_mghsettings.EN_SITEDIR+"b2kyero.xml", "w")
		file.write(outputText)
		file.close()
'''
	print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
	for props in propdict['props']:
			print props
'''
