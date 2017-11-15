#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys);
sys.setdefaultencoding("utf8")
sys.path.insert(0, './')
import jinja2
import os
import _mghsettings
import _mgh_data

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

#template setup detail.jinja
templateLoader = jinja2.FileSystemLoader(_mghsettings.IV_NL_TEMPLATEFOLDER)
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "iv_nl_detail.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

#loop for each property record in the database
for prop in _mgh_data.props:
	row = _mgh_data.props[prop]
	#for each prop get the pic urls for slideshow
	firsturl = row['pics'][0].replace('/s640/','/s0/').replace('s640-rj-e30-v2','s0-rj-e30-l80')
	picurldictlist = []
	slidecount = 1
	for i, pic in enumerate(row['pics']):
	    row['pics'][i] = pic.replace('/s0/','/s35-p/').replace('/s640/','/s35-p/').replace('s640-rj-e30-v2','s35-p-rj-e30-l80')

	for pic in row['pics']:
	    picurldict = {}
	    picurldict['slide'] = slidecount
	    picurldict['src'] = pic
	    picurldictlist.append(picurldict)
	    slidecount += 1

    #prepare the vars to pass to the template

	if row['rental'] == 'True':
		saleorrent = 'te huur'
	else:
		saleorrent = 'te koop'

	nl_proptype = _mghsettings.trans_proptypes[row['ptype'].lower()]['nl']
	de_proptype = _mghsettings.trans_proptypes[row['ptype'].lower()]['de']
	fr_proptype = _mghsettings.trans_proptypes[row['ptype'].lower()]['fr']

	propurl_de = '/'+str(row['beds'])+'-bad-'+de_proptype.replace(' ','-')+'-in-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
	propurl_nl = '/'+str(row['beds'])+'-slaapkamer-'+nl_proptype.replace(' ','-')+'-in-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
	propurl_fr = '/'+str(row['beds'])+'-chambre-'+fr_proptype.replace(' ','-').replace('é','e')+'-a-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
	propurl_en = '/'+str(row['beds'])+'-bed-'+row['ptype'].replace(' ','-')+'-in-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
	pagename = str(row['beds'])+'-slaapkamer-'+nl_proptype.replace(' ','-')+'-in-'+row['location'].replace(' ','-')+'-'+row['pid']
	if row['pool'].lower() == 'yes':
		pool = 'ja'
	else:
		pool = 'nee'
	propdict = {}
	propdict['props'] = []
	#propdict['propdescription'] = removeumlauts(row['strdescription_NL'])
	propdict['propdescription'] = row['NL']
	propdict['saleorrent'] = saleorrent
	propdict['beds'] = row['beds']
	if int(row['beds']) == 1:
		slaapkamer = ' slaapkamer'
	elif int(row['beds']) > 1:
		slaapkamer = ' slaapkamers'
	propdict['slaapsingplur'] = slaapkamer
	propdict['baths'] = row['baths']
	if int(row['baths']) == 1:
		badkamer = ' badkamer'
	elif int(row['baths']) > 1:
		badkamer = ' badkamers'
	propdict['badsingplur'] = badkamer
	propdict['livingarea'] = row['living']
	propdict['plotsize'] = row['plot']
	propdict['pool'] = row['pool']#pool
	propdict['propid'] = row['pid']
	propdict['propref'] = row['ref']
	propdict['propurl_de'] = propurl_de
	propdict['propurl_en'] = propurl_en
	propdict['propurl_fr'] = propurl_fr
	propdict['locationdetail']=row['location']
	propdict['province']=row['province']
	propdict['proptype']=nl_proptype
	propdict['saleorrent']=saleorrent
	pricefrom = ''
	if row['frequency'] == 'sale':
		propdict['frequency'] = ''
	elif row['frequency'] == 'month':
		propdict['frequency']= ' per maand'
	else:
		propdict['frequency']= ' per week'
		pricefrom = ' vanaf '

	propdict['underoffersold'] = row['salestage']
	if row['salestage'] == '0' or row['salestage'] == '10':
		propdict['price'] = pricefrom+"<span class='price_eur'>&euro;"+"{:,}".format(int(row['price']))+"</span> "
	elif row['salestage'] == '2':
		propdict['price'] = 'VERKOCHT'
	elif row['salestage'] == '3':
		propdict['price'] = '<span style="color:red;">VERHUURD</span>'
		propdict['frequency'] = ''
	else:
		propdict['price'] = ''
	propdict['firstimg'] = firsturl
	propdict['images'] = picurldictlist #prop['slide'],prop['src']

	outputText = template.render(propdict)
	file = open(_mghsettings.IV_NL_SITEDIR+pagename+".html", "w")
	file.write(outputText)
	file.close()
