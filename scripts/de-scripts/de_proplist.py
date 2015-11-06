#!/usr/bin/python
# -*- coding: utf-8 -*-
import jinja2
import os
import sqlite3
import _de_rubrunsdata
import sys
reload(sys);
sys.setdefaultencoding("utf8")
import _mghsettings

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

templateLoader = jinja2.FileSystemLoader(_mghsettings.DE_TEMPLATEFOLDER)
templateEnv = jinja2.Environment( loader=templateLoader )

TEMPLATE_FILE = "de_proplist.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

db=sqlite3.connect(_mghsettings.DATAFOLDER+'mgh.db')
db.row_factory = sqlite3.Row
cursor=db.cursor()

def getpropfirstpic(album):
	myfile = open(_mghsettings.PICFOLDER+row['strpropertyid']+".pics","r")
	mylines = list(myfile)
	myfile.close()
	return mylines[0].replace('/s0/','/s400/')

def makepage(propdict,prevpage,nextpage,thispage, pagename, pagename_nl, pagename_en):
	propdict['prevpage'] = pagename+str(prevpage)+".html"
	propdict['nextpage'] = pagename+str(nextpage)+".html"
	propdict['url_en'] = pagename_en+str(thispage)+".html"
	propdict['url_nl'] = pagename_nl+str(thispage)+".html"
	outputText = template.render(propdict)
	#print outputText
	file = open(_mghsettings.DE_SITEDIR+pagename+str(thispage)+".html", "w")
	file.write(outputText)
	file.close()

def removeumlauts(text):
	outchars = {u'\xb4':'&acute;',u'\u20ac':'&euro;',u'\xe1':'a',u'\xf1':'n',u'\xed':'i',u'\u2013':'',u'\xa8':'',u'\xad':'-',u'Ä':'&Auml;',u'ä':'&auml;',u'Ë':'&Euml;',u'ë':'&euml;',u'Ï':'&Iuml;',u'ï':'&iuml;',u'Ö':'&Ouml;',u'ö':'&ouml;',u'ß':'&szlig;',u'Ü':'&Uuml;',u'ü':'&uuml;'}
	for i, j in outchars.iteritems():
		text = text.replace(i, j)
	return text

for rubrun in _de_rubrunsdata.rubruns:
	topsixdict = {}
	topsixdict['title'] = rubrun['title']
	topsixdict['keywords'] = rubrun['keywords']
	topsixdict['description'] = rubrun['description']
	topsixdict['props'] = []


	cursor.execute(rubrun['query']) # LIMIT 20
	propstoprocess = len(cursor.fetchall())
	cursor.execute(rubrun['query']) # LIMIT 20
	print propstoprocess
	rowcount = 0
	pagecount = 0
	for row in cursor:
		rowcount = rowcount + 1
		#nl_proptype = _mghsettings.trans_proptypes[row['strpropertytype'].lower()]['nl']
		de_proptype = _mghsettings.trans_proptypes[row['strpropertytype'].lower()]['de']
		#propurl_nl = '/'+str(row['intbeds'])+'-slaapkamer-'+nl_proptype.replace(' ','-').replace('&auml;','a')+'-in-'+row['strlocation_detail'].replace(' ','-')+'-'+row['strpropertyid']+'.html'
		propurl = '/'+str(row['intbeds'])+'-bad-'+de_proptype.replace(' ','-').replace('&auml;','a')+'-in-'+row['strlocation_detail'].replace(' ','-')+'-'+row['strpropertyid']+'.html'

		if row['blnrental'] == 1:
			saleorrent = 'zu vermieten'
		else:
			saleorrent = 'zu verkaufen'
		prop = {}
		#prop['description'] = removeumlauts(row['strdescription_DE'][:400])
		prop['description'] = row['strdescription_DE'][:400]
		prop['beds'] = row['intbeds']
		prop['baths'] = row['intbaths']
		prop['propid'] = row['strpropertyid']
		prop['propref'] = row['strpropertyref']
		prop['propurl'] = propurl
		prop['locationdetail']=row['strlocation_detail']
		prop['proptype']= de_proptype
		prop['saleorrent']=saleorrent
		if row['strFrequency'] == 'week':
			prop['frequency'] = ' je Woche'
		elif row['strFrequency'] == 'month':
			prop['frequency'] = ' je Monat'
		else:
			prop['frequency']= ''
		prop['underoffersold'] = row['intunderoffersold']
		if row['intunderoffersold'] == 0:
			prop['price'] = "<span class='price_eur'>&euro;"+"{:,}".format(row['intprice'])+"</span> "
		elif row['intunderoffersold'] == 2:
			prop['price'] = 'verkauft'
		elif row['intunderoffersold'] == 3:
			prop['price'] = '<span style="color:red;">VERMIETET</span>'
			prop['frequency'] = ''
		else:
			prop['price'] = ''
		prop['img'] = getpropfirstpic(row['strpropertyid'])
		topsixdict['props'].append(prop)

		if rowcount == _mghsettings.PPP:
			rowcount = 0
			propstoprocess = propstoprocess - _mghsettings.PPP
			print propstoprocess
			pagenext = pagecount+1
			pageprev = pagecount-1
			if propstoprocess < _mghsettings.PPP:
				pagenext = 0
			if pageprev < 0:
				pageprev = 0
			makepage(topsixdict,pageprev,pagenext,pagecount,rubrun['pagename'],rubrun['pagename_nl'],rubrun['pagename_en'])
			pagecount = pagecount + 1
			topsixdict['props'] = []



	if len(topsixdict) > 0:
		makepage(topsixdict,pagecount-1,0,pagecount,rubrun['pagename'],rubrun['pagename_nl'],rubrun['pagename_en'])



#for item in topsixdict['props']:
	#for key in item:
		#print item[key]

	#"""

	#title 'Villamartin Property for Sale, Playa Flamenca, Cabo Roig, Guardamar del Segura, Ciudad Quesada Costa Blanca Spain'
	#keywords 'Villamartin Property for sale, Playa Flamenca, Cabo Roig, Guardamar del Segura and Ciudad Quesada'
	#description  'Property for sale in Villamartin, Playa Flamenca, Cabo Roig, Los Altos, Los Balcones, Guardamar del Segura, Ciudad Quesada in Torrevieja and  Orihuela Costa areas of Southern Costa Blanca Spain, '

	#propurl '/'+row['strpropertyid']+'-'+row['intbeds']+' bed '+row['strpropertytype']+' in '+row['strlocation_detail']+'.html'
	#locationdetail row['strlocation_detail']
	#proptype row['strpropertytype']
	#saleorrent if row['blnrental'] == 1 saleorrent = 'For rent' else saleorrent = 'For Sale'
	#price row['intprice']

	#"""
