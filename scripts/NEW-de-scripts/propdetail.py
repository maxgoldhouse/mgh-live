#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys);
sys.setdefaultencoding("utf8")
sys.path.insert(0, './')
import jinja2
import os
import time
#-#from mghmodules import _mghsettings
#-#from mghmodules import _mgh_data
import _mghsettings
import _mgh_data

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

#template setup detail.jinja
templateLoader = jinja2.FileSystemLoader(_mghsettings.NEWDE_TEMPLATEFOLDER)
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "detail.html"

template = templateEnv.get_template( TEMPLATE_FILE )

#loop for each property record in the database
for prop in _mgh_data.props:
	thisprop = _mgh_data.props[prop]
	#print thisprop['ref']
	#for each prop get the pic urls for slideshow
	#get the first url from  picurllist
	firsturl = thisprop['pics'][0]

	#for each prop get the pic urls for slideshow
	picurldictlist = []
	slidecount = 1
	for i, pic in enumerate(thisprop['pics']):
    	#thisprop['pics'][i] = pic.replace('/s0/','/s640-e30-rj-l80/').replace('/s640/','/s640-e30-rj-l80/')
	    thisprop['pics'][i] = pic.replace('/s0/','/s640-e30-rj-l80/').replace('/s640/','/s640-e30-rj-l80/')

	for pic in thisprop['pics']:
	    picurldict = {}
	    picurldict['slide'] = slidecount
	    picurldict['src'] = pic
	    picurldictlist.append(picurldict)
	    slidecount += 1

    #prepare the vars to pass to the template
	#print 'propid ' + thisprop['pid']
	#print 'price ' + thisprop['price']

	if thisprop['rental'] == 'True':
		saleorrent = 'zu vermieten'
	else:
		saleorrent = 'zu verkaufen'

	nl_proptype = _mghsettings.trans_proptypes[thisprop['ptype'].lower()]['nl']
	de_proptype = _mghsettings.trans_proptypes[thisprop['ptype'].lower()]['de']
	fr_proptype = _mghsettings.trans_proptypes[thisprop['ptype'].lower()]['fr']

	propurl_de = '/'+str(thisprop['beds'])+'-Schlafzimmer-'+de_proptype.replace(' ','-')+'-in-'+thisprop['location'].replace(' ','-')+'-'+thisprop['pid']+'.html'
	propurl_nl = '/'+str(thisprop['beds'])+'-slaapkamer-'+nl_proptype.replace(' ','-')+'-in-'+thisprop['location'].replace(' ','-')+'-'+thisprop['pid']+'.html'
	propurl_fr = '/'+str(thisprop['beds'])+'-chambre-'+fr_proptype.replace(' ','-').replace('é','e')+'-a-'+thisprop['location'].replace(' ','-')+'-'+thisprop['pid']+'.html'
	propurl_en = '/'+str(thisprop['beds'])+'-bed-'+thisprop['ptype'].replace(' ','-')+'-in-'+thisprop['location'].replace(' ','-')+'-'+thisprop['pid']+'.html'
	pagename = str(thisprop['beds'])+'-Schlafzimmer-'+de_proptype.replace(' ','-')+'-in-'+thisprop['location'].replace(' ','-')+'-'+thisprop['pid']
	if thisprop['pool'].lower() == 'yes':
		pool = 'Ja'
	elif thisprop['pool'].lower() == 'no':
		pool = 'Nein'
	else:
		pool = thisprop['pool']
	propdict = {}
	propdict['props'] = []
	propdict['propdescription'] = thisprop['DE']
	propdict['offplan'] = thisprop['offplan']
	propdict['saleorrent'] = saleorrent
	propdict['beds'] = thisprop['beds']
	if int(thisprop['beds']) == 1:
		Schlafzimmer = ' Schlafzimmer'
	elif int(thisprop['beds']) > 1:
		Schlafzimmer = ' Schlafzimmer'
	propdict['slaapsingplur'] = Schlafzimmer
	propdict['baths'] = thisprop['baths']
	if int(thisprop['baths']) == 1:
		Badezimmer = ' Badezimmer'
	elif int(thisprop['baths']) > 1:
		Badezimmer = ' Badezimmer'
	propdict['badsingplur'] = Badezimmer
	propdict['livingarea'] = thisprop['living']
	propdict['plotsize'] = thisprop['plot']
	propdict['pool'] = pool
	propdict['propid'] = thisprop['pid']
	propdict['propref'] = thisprop['ref']
	propdict['propurl_de'] = propurl_de
	propdict['propurl_en'] = propurl_en
	propdict['propurl_nl'] = propurl_nl
	propdict['propurl_fr'] = propurl_fr
	propdict['locationdetail']=thisprop['location']
	propdict['province']=thisprop['province']
	propdict['proptype']=de_proptype
	propdict['saleorrent']=saleorrent
	pricefrom = ''
	if thisprop['frequency'] == 'sale':
		propdict['frequency'] = ''
	elif thisprop['frequency'] == 'month':
		propdict['frequency']= ' pro Monat'
	else:
		propdict['frequency']= ' pro Woche'
		pricefrom = ' von '

	propdict['underoffersold'] = thisprop['salestage']
	if thisprop['salestage'] == '0' or thisprop['salestage'] == '10':
		propdict['price'] = pricefrom+"<span class='price_eur'>&euro;"+"{:,}".format(int(thisprop['price']))+"</span> "
	elif thisprop['salestage'] == '2':
		propdict['price'] = 'VERKAUFT'
	elif thisprop['salestage'] == '3':
		propdict['price'] = '<span style="color:red;">GEMIETET</span>'
		propdict['frequency'] = ''
	else:
		propdict['price'] = ''
	propdict['firstimg'] = firsturl
	propdict['images'] = picurldictlist #prop['slide'],prop['src']
	propdict['moredetails'] = thisprop['moredetails']
	propdict['timestamp'] = str(int(time.time()))

	#if thisprop.has_key("moredetails"):
	#	propdict['moredetails'] = thisprop['moredetails']
	#else:
	#	propdict['moredetails'] = ' end.'

	outputText = template.render(propdict)
	file = open(_mghsettings.NEWDE_SITEDIR+pagename+".html", "w")
	file.write(outputText)
	file.close()