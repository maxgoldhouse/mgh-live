#!/usr/bin/python
# -*- coding: utf-8 -*-

import jinja2
import os
import sqlite3
import sys
reload(sys);
sys.setdefaultencoding("utf8")
import _mghsettings

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

#template setup detail.jinja
templateLoader = jinja2.FileSystemLoader(_mghsettings.DE_TEMPLATEFOLDER)
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "de_detail.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

def removeumlauts(text):
	outchars = {u'\xb4':'&acute;',u'\u20ac':'&euro;',u'\xe1':'a',u'\xf1':'n',u'\xed':'i',u'\u2013':'',u'\xa8':'',u'\xad':'-',u'Ä':'&Auml;',u'ä':'&auml;',u'Ë':'&Euml;',u'ë':'&euml;',u'Ï':'&Iuml;',u'ï':'&iuml;',u'Ö':'&Ouml;',u'ö':'&ouml;',u'ß':'&szlig;',u'Ü':'&Uuml;',u'ü':'&uuml;'}
	for i, j in outchars.iteritems():
		text = text.replace(i, j)
	return text

db=sqlite3.connect(_mghsettings.DATAFOLDER+'mgh.db')
db.row_factory = sqlite3.Row
cursor=db.cursor()

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

	if row['blnrental'] == 1:
		saleorrent = 'zu vermieten'
	else:
		saleorrent = 'zu verkaufen'

	de_proptype = _mghsettings.trans_proptypes[row['strpropertytype'].lower()]['de']
	nl_proptype = _mghsettings.trans_proptypes[row['strpropertytype'].lower()]['nl']
	pagename = str(row['intbeds'])+'-bad-'+de_proptype.replace(' ','-').replace('&auml;','a')+'-in-'+row['strlocation_detail'].replace(' ','-')+'-'+row['strpropertyid']
	propurl_nl = '/'+str(row['intbeds'])+'-slaapkamer-'+nl_proptype.replace(' ','-').replace('&auml;','a')+'-in-'+row['strlocation_detail'].replace(' ','-')+'-'+row['strpropertyid']+'.html'
	#propurl_de = '/'+str(row['intbeds'])+'-bad-'+de_proptype.replace(' ','-').replace('&auml;','a')+'-in-'+row['strlocation_detail'].replace(' ','-')+'-'+row['strpropertyid']+'.html'
	propurl_en = '/'+str(row['intbeds'])+'-bed-'+row['strpropertytype'].replace(' ','-')+'-in-'+row['strlocation_detail'].replace(' ','-')+'-'+row['strpropertyid']+'.html'
	if row['strpool'].lower() == 'yes':
		pool = 'ja'
	else:
		pool = 'nein'
	propdict = {}
	propdict['props'] = []
	#propdict['propdescription'] = removeumlauts(row['strdescription_DE'])
	propdict['propdescription'] = row['strdescription_DE']
	propdict['saleorrent'] = saleorrent
	propdict['beds'] = row['intbeds']
	propdict['baths'] = row['intbaths']
	propdict['livingarea'] = row['intlivingarea']
	propdict['plotsize'] = row['intplotsize']
	propdict['pool'] = pool
	propdict['propid'] = row['strpropertyid']
	propdict['propref'] = row['strpropertyref']
	propdict['propurl_nl'] = propurl_nl
	propdict['propurl_en'] = propurl_en
	propdict['locationdetail']=row['strlocation_detail']
	propdict['province']=row['strprovince']
	propdict['proptype']=de_proptype
	propdict['saleorrent']=saleorrent
	if row['strFrequency'] == 'week':
		propdict['frequency'] = ' je Woche'
	elif row['strFrequency'] == 'month':
		propdict['frequency'] = ' je Monat'
	else:
		propdict['frequency']= ''
	propdict['underoffersold'] = row['intunderoffersold']
	if row['intunderoffersold'] == 0:
		propdict['price'] = "<span class='price_eur'>&euro;"+"{:,}".format(row['intprice'])+"</span> "
	elif row['intunderoffersold'] == 2:
		propdict['price'] = 'verkauft'
	elif row['intunderoffersold'] == 3:
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
