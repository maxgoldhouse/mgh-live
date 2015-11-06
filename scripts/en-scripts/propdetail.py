#!/usr/bin/python
# -*- coding: utf-8 -*-
import jinja2
import os
import sqlite3
import _mghsettings
import sys
reload(sys);
sys.setdefaultencoding("utf8")

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

#template setup detail.jinja
templateLoader = jinja2.FileSystemLoader(_mghsettings.EN_TEMPLATEFOLDER)
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "detail.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

db=sqlite3.connect(_mghsettings.DATAFOLDER+'mgh.db')
db.row_factory = sqlite3.Row
cursor=db.cursor()

def removenonascci(text):
	outchars = {u'\xb4':'&acute;',u'\u20ac':'&euro;',u'\xe1':'a',u'\xf1':'n',u'\xed':'i',u'\u2013':'',u'\xa8':'',u'\xad':'-'}
	for i, j in outchars.iteritems():
		text = text.replace(i, j)
	return text

def removeumlauts(text):
	outchars = {u'\xb4':'&acute;',u'\u20ac':'&euro;',u'\xe1':'a',u'\xf1':'n',u'\xed':'i',u'\u2013':'',u'\xa8':'',u'\xad':'-',u'Ä':'&Auml;',u'ä':'&auml;',u'Ë':'&Euml;',u'ë':'&euml;',u'Ï':'&Iuml;',u'ï':'&iuml;',u'Ö':'&Ouml;',u'ö':'&ouml;',u'ß':'&szlig;',u'Ü':'&Uuml;',u'ü':'&uuml;'}
	for i, j in outchars.iteritems():
		text = text.replace(i, j)
	return text

#Get the data from the database
cursor.execute("SELECT * FROM  mghprops WHERE  blndisplay = 1")
#loop for each property record in the database
for row in cursor:
	#for each prop get the pic urls for slideshow
	file = open(_mghsettings.PICFOLDER+row['strpropertyid']+'.pics', 'r')
	picurllist = file.readlines()
	#get the first url from  picurllist
	firsturl = picurllist[0].replace('\n', '')

	picurldictlist = []
	slidecount = 1
	for i, line in enumerate(picurllist):
	    picurllist[i] = line.replace('/s0/','/s35-p/')

	for line in picurllist:
	    picurldict = {}
	    picurldict['slide'] = slidecount
	    picurldict['src'] = line
	    picurldictlist.append(picurldict)
	    slidecount += 1

    #prepare the vars to pass to the template
	print 'propid ' + row['strpropertyid']
	if row['blnrental'] == 1:
		saleorrent = 'rent'
	else:
		saleorrent = 'sale'

	pagename = str(row['intbeds'])+'-bed-'+row['strpropertytype'].replace(' ','-')+'-in-'+row['strlocation_detail'].replace(' ','-')+'-'+row['strpropertyid']
	de_proptype = _mghsettings.trans_proptypes[row['strpropertytype'].lower()]['de']
	nl_proptype = _mghsettings.trans_proptypes[row['strpropertytype'].lower()]['nl']
	fr_proptype = _mghsettings.trans_proptypes[row['strpropertytype'].lower()]['fr']
	propurl_de = '/'+str(row['intbeds'])+'-bad-'+de_proptype.replace(' ','-')+'-in-'+row['strlocation_detail'].replace(' ','-')+'-'+row['strpropertyid']+'.html'
	propurl_nl = '/'+str(row['intbeds'])+'-slaapkamer-'+nl_proptype.replace(' ','-')+'-in-'+row['strlocation_detail'].replace(' ','-')+'-'+row['strpropertyid']+'.html'
	propurl_fr = '/'+str(row['intbeds'])+'-chambre-'+fr_proptype.replace(' ','-').replace('é','e')+'-a-'+row['strlocation_detail'].replace(' ','-')+'-'+row['strpropertyid']+'.html'
	#print propurl_nl
	propurl_en = '/'+str(row['intbeds'])+'-bed-'+row['strpropertytype'].replace(' ','-')+'-in-'+row['strlocation_detail'].replace(' ','-')+'-'+row['strpropertyid']+'.html'
	propdict = {}
	propdict['props'] = []
	propdict['propdescription'] = row['strdescription']
	propdict['propdescription'] = removenonascci(row['strdescription'])
	propdict['saleorrent'] = saleorrent
	propdict['beds'] = row['intbeds']
	propdict['baths'] = row['intbaths']
	propdict['livingarea'] = row['intlivingarea']
	propdict['plotsize'] = row['intplotsize']
	propdict['pool'] = row['strpool']
	propdict['propid'] = row['strpropertyid']
	propdict['propref'] = row['strpropertyref']
	propdict['propurl_de'] = propurl_de
	propdict['propurl_en'] = propurl_en
	propdict['propurl_nl'] = propurl_nl
	propdict['propurl_fr'] = propurl_fr
	propdict['locationdetail']=row['strlocation_detail']
	propdict['province']=row['strprovince']
	propdict['proptype']=row['strpropertytype']
	propdict['saleorrent']=saleorrent
	if row['strFrequency'] == 'sale':
		propdict['frequency'] = ''
	else:
		propdict['frequency']= ' per '+row['strFrequency']
	propdict['underoffersold'] = row['intunderoffersold']
	if row['intunderoffersold'] == 0:
		propdict['price'] = "<span class='price_eur'>&euro;"+"{:,}".format(row['intprice'])+"</span> "
		propdict['mp'] = ''
		if row['blnrental'] == 0:
			p = row['intprice']*_mghsettings.MORTGAGE_LTV
			deposit = row['intprice']*(1-_mghsettings.MORTGAGE_LTV)
			propdict['deposit'] = "<span class='price_eur propopt'>&euro;"+"{:,}".format(int(round(deposit,0)))+"</span>"
			i = _mghsettings.MORTGAGE_INTEREST
			mi = i/(100 * 12) # monthly interest
			y = _mghsettings.MORTGAGE_TERM
			months = y * 12
			mp = p * ( mi / (1 - (1 + mi) ** (- months))) # monthly payment
			propdict['mp'] = "<span class='price_eur propopt'>&euro;"+"{:,}".format(int(round(mp,0)))+"</span>"
	elif row['intunderoffersold'] == 2:
		propdict['price'] = 'SOLD'
	elif row['intunderoffersold'] == 3:
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
