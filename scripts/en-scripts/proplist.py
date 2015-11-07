#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys);
sys.setdefaultencoding("utf8")
sys.path.insert(0, '/home/papo/projects/mgh-live')
import jinja2
import os
import _all_rubrunsdata
import _mghsettings
import _mgh_data



THIS_DIR = os.path.dirname(os.path.abspath(__file__))
templateLoader = jinja2.FileSystemLoader(_mghsettings.EN_TEMPLATEFOLDER)
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "proplist.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

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

for rub in _all_rubrunsdata.rubruns:
	topsixdict = {}
	topsixdict['title'] = rub["EN"]['title']
	topsixdict['keywords'] = rub["EN"]['keywords']
	topsixdict['description'] = rub["EN"]['description']
	topsixdict['h1'] = rub["EN"]['h1']
	topsixdict['props'] = []

	rowcount = 0
	pagecount = 0
	for propinlist in _mgh_data.proplists[rub['rubrun']]:# LIMIT 20
		rowcount = rowcount + 1
		thisprop = _mgh_data.props[str(propinlist)]
		propurl = '/'+str(thisprop['beds'])+'-bed-'+thisprop['ptype'].replace(' ','-')+'-in-'+thisprop['location'].replace(' ','-')+'-'+thisprop['pid']+'.html'
		if thisprop['rental'] == "True":
		  saleorrent = 'rent'
		else:
		  saleorrent = 'sale'
		prop = {}
		prop['description'] = thisprop['description'][:400]
		prop['beds'] = thisprop['beds']
		prop['baths'] = thisprop['baths']
		prop['propid'] = thisprop['pid']
		prop['propref'] = thisprop['ref']
		prop['propurl'] = propurl
		prop['locationdetail']=thisprop['location']
		prop['proptype']=thisprop['ptype']
		if thisprop['frequency'] == 'sale':
			prop['frequency'] = ''
		else:
			prop['frequency']= ' per '+thisprop['frequency']
		prop['underoffersold'] = thisprop['salestage']
		if thisprop['salestage'] == '0':
			prop['price'] = "<span class='price_eur'>&euro;"+"{:,}".format(int(thisprop['price']))+"</span> "
			prop['saleorrent'] = saleorrent
			prop['mp'] = ''
			#if thisprop['rental'] == "False":

		elif thisprop['salestage'] == '2':
			prop['price'] = 'SOLD'
		elif thisprop['salestage'] == '3':
			prop['price'] = '<span style="color:red;">RENTED</span>'
			prop['frequency']= ''
		else:
			prop['price'] = ''
		prop['img'] = thisprop['pics'][0].replace('s0','s400')
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
			makepage(topsixdict,pageprev,pagenext,pagecount,rub['pagename_en'],rub['pagename_de'],rub['pagename_nl'],rub['pagename_fr'])
			pagecount = pagecount + 1
			topsixdict['props'] = []



	if len(topsixdict) > 0:
		makepage(topsixdict,pagecount-1,0,pagecount,rub['pagename_en'],rub['pagename_de'],rub['pagename_nl'],rub['pagename_fr'])



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
