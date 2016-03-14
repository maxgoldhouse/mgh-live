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
templateLoader = jinja2.FileSystemLoader(_mghsettings.DE_TEMPLATEFOLDER)
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "de_detail.jinja"
template = templateEnv.get_template( TEMPLATE_FILE )


#Get the data from the database
#loop for each property record in the database
for prop in _mgh_data.props:
	row = _mgh_data.props[prop]
	#print thisprop['ref']
	#for each prop get the pic urls for slideshow
	#get the first url from  picurllist
	firsturl = row['pics'][0]
	#for each prop get the pic urls for slideshow
	picurldictlist = []
	slidecount = 1
	for i, pic in enumerate(row['pics']):
	    row['pics'][i] = pic.replace('/s0/','/s35-p/')

	for pic in row['pics']:
	    picurldict = {}
	    picurldict['slide'] = slidecount
	    picurldict['src'] = pic
	    picurldictlist.append(picurldict)
	    slidecount += 1

    #prepare the vars to pass to the template

	if row['rental'] == 'True':
		saleorrent = 'zu vermieten'
	else:
		saleorrent = 'zu verkaufen'


	de_proptype = _mghsettings.trans_proptypes[row['ptype'].lower()]['de']
	nl_proptype = _mghsettings.trans_proptypes[row['ptype'].lower()]['nl']
	fr_proptype = _mghsettings.trans_proptypes[row['ptype'].lower()]['fr']
	propurl_de = '/'+str(row['beds'])+'-bad-'+de_proptype.replace(' ','-')+'-in-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
	propurl_nl = '/'+str(row['beds'])+'-slaapkamer-'+nl_proptype.replace(' ','-')+'-in-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
	propurl_fr = '/'+str(row['beds'])+'-chambre-'+fr_proptype.replace(' ','-').replace('é','e')+'-a-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
	propurl_en = '/'+str(row['beds'])+'-bed-'+row['ptype'].replace(' ','-')+'-in-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
	pagename = str(row['beds'])+'-bad-'+de_proptype.replace(' ','-').replace('&auml;','a')+'-in-'+row['location'].replace(' ','-')+'-'+row['pid']
	if row['pool'].lower() == 'yes':
		pool = 'ja'
	else:
		pool = 'nein'
	propdict = {}
	propdict['props'] = []
	propdict['propdescription'] = row['DE']
	propdict['saleorrent'] = saleorrent
	propdict['beds'] = row['beds']
	propdict['baths'] = row['baths']
	propdict['livingarea'] = row['living']
	propdict['plotsize'] = row['plot']
	propdict['pool'] = row['pool']
	propdict['propid'] = row['pid']
	propdict['propref'] = row['ref']
	propdict['propurl_nl'] = propurl_nl
	propdict['propurl_en'] = propurl_en
	propdict['propurl_fr'] = propurl_fr
	propdict['propurl_de'] = propurl_de
	propdict['locationdetail']=row['location']
	propdict['province']=row['province']
	propdict['proptype']=de_proptype
	propdict['saleorrent']=saleorrent
	pricefrom = ''
	if row['frequency'] == 'sale':
		propdict['frequency'] = ''
	elif row['frequency'] == 'month':
		propdict['frequency']= ' je Monat'
	else:
		propdict['frequency']= ' je Woche'
		pricefrom = ' von '

	propdict['underoffersold'] = row['salestage']
	if row['salestage'] == '0':
		propdict['price'] = pricefrom+"<span class='price_eur'>&euro;"+"{:,}".format(int(row['price']))+"</span> "
	elif row['salestage'] == '2':
		propdict['price'] = 'verkauft'
	elif row['salestage'] == '3':
		propdict['price'] = '<span style="color:red;">VERMIETET</span>'
		propdict['frequency'] = ''
	else:
		propdict['price'] = ''
	propdict['firstimg'] = firsturl
	propdict['images'] = picurldictlist #prop['slide'],prop['src']

	outputText = template.render(propdict)
	file = open(_mghsettings.DE_SITEDIR+pagename+".html", "w")
	file.write(outputText)
	file.close()
