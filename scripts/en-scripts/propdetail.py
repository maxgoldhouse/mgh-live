#!/usr/bin/python
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
templateLoader = jinja2.FileSystemLoader(_mghsettings.EN_TEMPLATEFOLDER)
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "detail.jinja"

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
	    thisprop['pics'][i] = pic.replace('/s0/','/s640-e30-v1/').replace('/s640/','/s640-e30-v1/')

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
		saleorrent = 'rent'
	else:
		saleorrent = 'sale'

	pagename = str(thisprop['beds'])+'-bed-'+thisprop['ptype'].replace(' ','-')+'-in-'+thisprop['location'].replace(' ','-')+'-'+thisprop['pid']
	de_proptype = _mghsettings.trans_proptypes[thisprop['ptype'].lower()]['de']
	nl_proptype = _mghsettings.trans_proptypes[thisprop['ptype'].lower()]['nl']
	fr_proptype = _mghsettings.trans_proptypes[thisprop['ptype'].lower()]['fr']
	propurl_de = '/'+str(thisprop['beds'])+'-bad-'+de_proptype.replace(' ','-')+'-in-'+thisprop['location'].replace(' ','-')+'-'+thisprop['pid']+'.html'
	propurl_nl = '/'+str(thisprop['beds'])+'-slaapkamer-'+nl_proptype.replace(' ','-')+'-in-'+thisprop['location'].replace(' ','-')+'-'+thisprop['pid']+'.html'
	propurl_fr = '/'+str(thisprop['beds'])+'-chambre-'+fr_proptype.replace(' ','-').replace('é','e')+'-a-'+thisprop['location'].replace(' ','-')+'-'+thisprop['pid']+'.html'
	#print propurl_nl
	propurl_en = '/'+str(thisprop['beds'])+'-bed-'+thisprop['ptype'].replace(' ','-')+'-in-'+thisprop['location'].replace(' ','-')+'-'+thisprop['pid']+'.html'
	propdict = {}
	propdict['props'] = []
	propdict['propdescription'] = thisprop['description']
	propdict['propdescription'] = thisprop['description']
	propdict['saleorrent'] = saleorrent
	propdict['beds'] = thisprop['beds']
	propdict['baths'] = thisprop['baths']
	propdict['livingarea'] = thisprop['living']
	propdict['plotsize'] = thisprop['plot']
	propdict['pool'] = thisprop['pool']
	propdict['propid'] = thisprop['pid']
	propdict['propref'] = thisprop['ref']
	propdict['propurl_de'] = propurl_de
	propdict['propurl_en'] = propurl_en
	propdict['propurl_nl'] = propurl_nl
	propdict['propurl_fr'] = propurl_fr
	propdict['locationdetail']=thisprop['location']
	propdict['province']=thisprop['province']
	propdict['proptype']=thisprop['ptype']
	propdict['saleorrent']=saleorrent
	pricefrom = ''
	if thisprop['frequency'] == 'sale':
		propdict['frequency'] = ''
	elif thisprop['frequency'] == 'month':
		propdict['frequency']= ' per '+thisprop['frequency']
	else:
		propdict['frequency']= ' per '+thisprop['frequency']
		pricefrom = ' from '

	propdict['underoffersold'] = thisprop['salestage']
	if thisprop['salestage'] == '0':
		propdict['price'] = pricefrom + "<span class='price_eur'>&euro;"+"{:,}".format(int(thisprop['price']))+"</span> "
		propdict['mp'] = ''
	elif thisprop['salestage'] == '2':
		propdict['price'] = 'SOLD'
	elif thisprop['salestage'] == '3':
		propdict['price'] = '<span style="color:red;">RENTED</span>'
		propdict['frequency']= ''
	else:
		propdict['price'] = ''
	propdict['firstimg'] = firsturl
	propdict['images'] = picurldictlist #prop['slide'],prop['src']

	outputText = template.render(propdict)
	file = open(_mghsettings.EN_SITEDIR+pagename+".html", "w")
	file.write(outputText)
	file.close()
