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

templateLoader = jinja2.FileSystemLoader(_mghsettings.FR_TEMPLATEFOLDER)
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "fr_detail.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

#loop for each property record in the database
for prop in _mgh_data.props:
	row = _mgh_data.props[prop]

	#for each prop get the pic urls for slideshow
	firsturl = row['pics'][0]
	picurldictlist = []
	slidecount = 1
	for i, pic in enumerate(row['pics']):
	    row['pics'][i] = pic.replace('s0','s35-p')

	for pic in row['pics']:
	    picurldict = {}
	    picurldict['slide'] = slidecount
	    picurldict['src'] = pic
	    picurldictlist.append(picurldict)
	    slidecount += 1

    #prepare the vars to pass to the template

	if row['rental'] == 'True':
		saleorrent = 'à louer'
	else:
		saleorrent = 'à vendre'

	nl_proptype = _mghsettings.trans_proptypes[row['ptype'].lower()]['nl']
	de_proptype = _mghsettings.trans_proptypes[row['ptype'].lower()]['de']
	fr_proptype = _mghsettings.trans_proptypes[row['ptype'].lower()]['fr']
	propurl_de = '/'+str(row['beds'])+'-bad-'+de_proptype.replace(' ','-')+'-in-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
	propurl_nl = '/'+str(row['beds'])+'-slaapkamer-'+nl_proptype.replace(' ','-')+'-in-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
	propurl_fr = '/'+str(row['beds'])+'-chambre-'+fr_proptype.replace(' ','-').replace('é','e')+'-a-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
	propurl_en = '/'+str(row['beds'])+'-bed-'+row['ptype'].replace(' ','-')+'-in-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
	pagename = str(row['beds'])+'-chambre-'+fr_proptype.replace(' ','-').replace('é','e')+'-a-'+row['location'].replace(' ','-')+'-'+row['pid']
	if row['pool'].lower() == 'yes':
		pool = 'Oui'
	else:
		pool = 'Non'
	propdict = {}
	propdict['props'] = []
	propdict['propdescription'] = row['FR']
	propdict['saleorrent'] = saleorrent
	propdict['beds'] = row['beds']
	if int(row['beds']) == 1:
		chambre = ' chambre'
	elif int(row['beds']) > 1:
		chambre = ' chambres'
	propdict['chabresingplur'] = chambre
	propdict['baths'] = row['baths']
	if int(row['baths']) == 1:
		bain = ' salle de bain'
	elif int(row['baths']) > 1:
		bain = ' salles de bains'
	propdict['bainsingplur'] = bain
	propdict['livingarea'] = row['living']
	propdict['plotsize'] = row['plot']
	propdict['pool'] = pool
	propdict['propid'] = row['pid']
	propdict['propref'] = row['ref']
	propdict['propurl_de'] = propurl_de
	propdict['propurl_en'] = propurl_en
	propdict['propurl_nl'] = propurl_nl
	propdict['locationdetail']=row['location']
	propdict['province']=row['province']
	propdict['proptype']=fr_proptype
	propdict['saleorrent']=saleorrent
	if row['frequency'] == 'week':
		propdict['frequency'] = ' par semaine'
	elif row['frequency'] == 'month':
		propdict['frequency'] = ' par mois'
	else:
		propdict['frequency']= ''
	propdict['underoffersold'] = row['salestage']
	if row['salestage'] == '0':
		propdict['price'] = "<span class='price_eur'>&euro;"+"{:,}".format(int(row['price']))+"</span> "
	elif row['salestage'] == '2':
		propdict['price'] = 'VENDU'
	elif row['salestage'] == '3':
		propdict['price'] = '<span style="color:red;">LOUE</span>'
		propdict['frequency'] = ''
	else:
		propdict['price'] = ''
	propdict['firstimg'] = firsturl
	propdict['images'] = picurldictlist

	outputText = template.render(propdict)
	file = open(_mghsettings.FR_SITEDIR+pagename+".html", "w")
	file.write(outputText)
	file.close()
