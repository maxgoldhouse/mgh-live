#!/usr/bin/python
# -*- coding: utf-8 -*-
import jinja2
import os
import sqlite3
import _all_rubrunsdata
import _mghsettings
import sys
reload(sys);
sys.setdefaultencoding("utf8")


THIS_DIR = os.path.dirname(os.path.abspath(__file__))

templateLoader = jinja2.FileSystemLoader(_mghsettings.EN_TEMPLATEFOLDER)
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "proplist.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

db=sqlite3.connect(_mghsettings.DATAFOLDER+'mgh.db')
db.row_factory = sqlite3.Row
cursor=db.cursor()


def getpropfirstpic(album):
	myfile = open(_mghsettings.PICFOLDER+row['strpropertyid']+".pics","r")
	mylines = list(myfile)
	myfile.close()
	return mylines[0].replace('/s0/','/s400/')

def makepage(propdict,prevpage,nextpage,thispage, pagename, pagename_de, pagename_nl, pagename_fr):
	propdict['prevpage'] = pagename+str(prevpage)+".html"
	propdict['nextpage'] = pagename+str(nextpage)+".html"
	propdict['url_en'] = pagename+str(thispage)+".html"
	propdict['url_de'] = pagename_de+str(thispage)+".html"
	propdict['url_nl'] = pagename_nl+str(thispage)+".html"
	propdict['url_fr'] = pagename_fr+str(thispage)+".html"
	outputText = template.render(propdict)
	#print 'page processing '+outputText
	file = open(_mghsettings.EN_SITEDIR+pagename+str(thispage)+".html", "w")
	file.write(outputText)
	file.close()

def removenonascci(text):
	outchars = {u'\xb4':'&acute;',u'\u20ac':'&euro;',u'\xe1':'a',u'\xf1':'n',u'\xed':'i',u'\u2013':'',u'\xa8':'',u'\xad':'-'}
	for i, j in outchars.iteritems():
		text = text.replace(i, j)
	return text

for rubrun in _all_rubrunsdata.rubruns:
	topsixdict = {}
	topsixdict['title'] = rubrun["EN"]['title']
	topsixdict['keywords'] = rubrun["EN"]['keywords']
	topsixdict['description'] = rubrun["EN"]['description']
	topsixdict['h1'] = rubrun["EN"]['h1']
	topsixdict['props'] = []


	cursor.execute(rubrun['query']) # LIMIT 20
	propstoprocess = len(cursor.fetchall())
	cursor.execute(rubrun['query']) # LIMIT 20
	print propstoprocess
	rowcount = 0
	pagecount = 0
	for row in cursor:
		rowcount = rowcount + 1

		propurl = '/'+str(row['intbeds'])+'-bed-'+row['strpropertytype'].replace(' ','-')+'-in-'+row['strlocation_detail'].replace(' ','-')+'-'+row['strpropertyid']+'.html'
		if row['blnrental'] == 1:
			saleorrent = 'rent'
		else:
			saleorrent = 'sale'
		prop = {}
		prop['description'] = removenonascci(row['strdescription'][:400])
		prop['beds'] = row['intbeds']
		prop['baths'] = row['intbaths']
		prop['propid'] = row['strpropertyid']
		prop['propref'] = row['strpropertyref']
		prop['propurl'] = propurl
		prop['locationdetail']=row['strlocation_detail']
		prop['proptype']=row['strpropertytype']
		if row['strFrequency'] == 'sale':
			prop['frequency'] = ''
		else:
			prop['frequency']= ' per '+row['strFrequency']
		prop['underoffersold'] = row['intunderoffersold']
		if row['intunderoffersold'] == 0:
			prop['price'] = "<span class='price_eur'>&euro;"+"{:,}".format(row['intprice'])+"</span> "
			prop['saleorrent'] = saleorrent
			prop['mp'] = ''
			if row['blnrental'] == 0:
				p = row['intprice']*_mghsettings.MORTGAGE_LTV
				deposit = row['intprice']*(1-_mghsettings.MORTGAGE_LTV)
				prop['deposit'] = "<span class='price_eur propopt'>&euro;"+"{:,}".format(int(round(deposit,0)))+"</span>"
				i = _mghsettings.MORTGAGE_INTEREST
				mi = i/(100 * 12) # monthly interest
				y = _mghsettings.MORTGAGE_TERM
				months = y * 12
				mp = p * ( mi / (1 - (1 + mi) ** (- months))) # monthly payment
				prop['mp'] = "<span class='price_eur propopt'>&euro;"+"{:,}".format(int(round(mp,0)))+"</span>"
		elif row['intunderoffersold'] == 2:
			prop['price'] = 'SOLD'
		elif row['intunderoffersold'] == 3:
			prop['price'] = '<span style="color:red;">RENTED</span>'
			prop['frequency']= ''
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
			makepage(topsixdict,pageprev,pagenext,pagecount,rubrun['pagename_en'],rubrun['pagename_de'],rubrun['pagename_nl'],rubrun['pagename_fr'])
			pagecount = pagecount + 1
			topsixdict['props'] = []



	if len(topsixdict) > 0:
		makepage(topsixdict,pagecount-1,0,pagecount,rubrun['pagename_en'],rubrun['pagename_de'],rubrun['pagename_nl'],rubrun['pagename_fr'])



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
