#!/usr/bin/python
# -*- coding: utf-8 -*-

import jinja2
import os
import sqlite3
import _fr_rubrunsdata
import sys
reload(sys);
sys.setdefaultencoding("utf8")
import _mghsettings



THIS_DIR = os.path.dirname(os.path.abspath(__file__))

templateLoader = jinja2.FileSystemLoader(_mghsettings.FR_TEMPLATEFOLDER)
templateEnv = jinja2.Environment( loader=templateLoader )

TEMPLATE_FILE = "fr_proplist.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

db=sqlite3.connect(_mghsettings.DATAFOLDER+'mgh.db')
db.row_factory = sqlite3.Row
cursor=db.cursor()

def getpropfirstpic(album):
	myfile = open(_mghsettings.PICFOLDER+row['strpropertyid']+".pics","r")
	mylines = list(myfile)
	myfile.close()
	return mylines[0].replace('/s0/','/s400/')

def makepage(propdict,prevpage,nextpage,thispage, pagename_nl, pagename_en, pagename_de, pagename_fr):
	propdict['prevpage'] = pagename_fr+str(prevpage)+".html"
	propdict['nextpage'] = pagename_fr+str(nextpage)+".html"
	propdict['url_en'] = pagename_en+str(thispage)+".html"
	propdict['url_de'] = pagename_de+str(thispage)+".html"
	propdict['url_nl'] = pagename_nl+str(thispage)+".html"
	outputText = template.render(propdict)
	#print outputText
	file = open(_mghsettings.FR_SITEDIR+pagename_fr+str(thispage).replace('é','e')+".html", "w")
	file.write(outputText)
	file.close()

def removeumlauts(text):
	outchars = {u'\xb4':'&acute;',u'\u20ac':'&euro;',u'\xe1':'a',u'\xf1':'n',u'\xed':'i',u'\u2013':'',u'\xa8':'',u'\xad':'-',u'Ä':'&Auml;',u'ä':'&auml;',u'Ë':'&Euml;',u'ë':'&euml;',u'Ï':'&Iuml;',u'ï':'&iuml;',u'Ö':'&Ouml;',u'ö':'&ouml;',u'ß':'&szlig;',u'Ü':'&Uuml;',u'ü':'&uuml;'}
	for i, j in outchars.iteritems():
		text = text.replace(i, j)
	return text

for rubrun in _fr_rubrunsdata.rubruns:
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
		fr_proptype = _mghsettings.trans_proptypes[row['strpropertytype'].lower()]['fr']
		propurl = '/'+str(row['intbeds'])+'-chambre-'+fr_proptype.replace(' ','-').replace('é','e')+'-a-'+row['strlocation_detail'].replace(' ','-')+'-'+row['strpropertyid']+'.html'
		if row['blnrental'] == 1:
			saleorrent = 'à louer'
		else:
			saleorrent = 'à vendre'
		prop = {}
		#prop['description'] = removeumlauts(row['strdescription_NL'][:400])
		prop['description'] = row['strdescription_FR'][:400]
		if row['intbeds'] == 1:
			chambre = ' chambre'
		elif row['intbeds'] > 1:
			chambre = ' chambres'
		prop['beds'] = str(row['intbeds']) + chambre
		if row['intbaths'] == 1:
			bain = ' salle de bain'
		elif row['intbaths'] > 1:
			bain = ' salles de bains'
		prop['baths'] = str(row['intbaths']) + bain
		prop['propid'] = row['strpropertyid']
		prop['propref'] = row['strpropertyref']
		prop['propurl'] = propurl
		prop['locationdetail']=row['strlocation_detail']
		prop['proptype']= fr_proptype
		prop['saleorrent']=saleorrent
		if row['strFrequency'] == 'week':
			prop['frequency'] = ' par semaine'
		elif row['strFrequency'] == 'month':
			prop['frequency'] = ' par mois'
		else:
			prop['frequency']= ''
		prop['underoffersold'] = row['intunderoffersold']
		if row['intunderoffersold'] == 0:
			prop['price'] = "<span class='price_eur'>&euro;"+"{:,}".format(row['intprice']).replace(',','.')+"</span> "
		elif row['intunderoffersold'] == 2:
			prop['price'] = 'VENDU'
		elif row['intunderoffersold'] == 3:
			prop['price'] = '<span style="color:red;">LOUE</span>'
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
			makepage(topsixdict,pageprev,pagenext,pagecount,rubrun['pagename_nl'],rubrun['pagename_en'], rubrun['pagename_de'], rubrun['pagename_fr'])
			pagecount = pagecount + 1
			topsixdict['props'] = []



	if len(topsixdict) > 0:
		makepage(topsixdict,pagecount-1,0,pagecount,rubrun['pagename_nl'],rubrun['pagename_en'],rubrun['pagename_de'], rubrun['pagename_fr'])
