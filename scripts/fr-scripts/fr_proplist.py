#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys);
sys.setdefaultencoding("utf8")
sys.path.insert(0, './')
import jinja2
import os
import _all_rubrunsdata
import _mghsettings
import _mgh_data

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

templateLoader = jinja2.FileSystemLoader(_mghsettings.FR_TEMPLATEFOLDER)
templateEnv = jinja2.Environment( loader=templateLoader )

TEMPLATE_FILE = "fr_proplist.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

def makepage(propdict,prevpage,nextpage,thispage, pagename_en, pagename_de, pagename_nl, pagename_fr):
	propdict['prevpage'] = pagename_fr+str(prevpage)+".html"
	propdict['nextpage'] = pagename_fr+str(nextpage)+".html"
	propdict['url_en'] = pagename_en+str(thispage)+".html"
	propdict['url_de'] = pagename_de+str(thispage)+".html"
	propdict['url_nl'] = pagename_nl+str(thispage)+".html"
	propdict['url_fr'] = pagename_fr+str(thispage)+".html"
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

for rubrun in _all_rubrunsdata.rubruns:
	topsixdict = {}
	topsixdict['title'] = rubrun["FR"]['title']
	topsixdict['keywords'] = rubrun["FR"]['keywords']
	topsixdict['description'] = rubrun["FR"]['description']
	topsixdict['h1'] = rubrun["FR"]['h1']
	topsixdict['props'] = []

	rowcount = 0
	pagecount = 0
	for propinlist in _mgh_data.proplists[rubrun['rubrun']]:
		rowcount = rowcount + 1
		row = _mgh_data.props[str(propinlist)]
		print row['pid']
		fr_proptype = _mghsettings.trans_proptypes[row['ptype'].lower()]['fr']
		propurl = '/'+str(row['beds'])+'-chambre-'+fr_proptype.replace(' ','-').replace('é','e').replace('â','a')+'-a-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
		if row['rental'] == 'True':
			saleorrent = 'à louer'
		else:
			saleorrent = 'à vendre'
		prop = {}
		if row['FR'][:400][-1] == '\xc3':
		  prop['description'] = row['FR'][:399]
		else:
		  prop['description'] = row['FR'][:400]
		if int(row['beds']) == 1:
			chambre = ' chambre'
		elif int(row['beds']) > 1:
			chambre = ' chambres'
		prop['beds'] = row['beds'] + chambre
		if int(row['baths']) == 1:
			bain = ' salle de bain'
		elif int(row['baths']) > 1:
			bain = ' salles de bains'
		prop['baths'] = row['baths'] + bain
		prop['propid'] = row['pid']
		prop['propref'] = row['ref']
		prop['propurl'] = propurl
		prop['locationdetail']=row['location']
		prop['proptype']= fr_proptype
		prop['saleorrent']=saleorrent
		pricefrom = ''
		if row['frequency'] == 'sale':
			prop['frequency'] = ''
		elif row['frequency'] == 'month':
			prop['frequency']= ' par mois'
		else:
			prop['frequency']= ' par semaine'
			pricefrom = ' à partir de '

		prop['underoffersold'] = row['salestage']
		if row['salestage'] == '0' or row['salestage'] == '10':
			prop['price'] = pricefrom+"<span class='price_eur'>&euro;"+"{:,}".format(int(row['price'])).replace(',','.')+"</span> "
		elif row['salestage'] == '2':
			prop['price'] = 'VENDU'
		elif row['salestage'] == '3':
			prop['price'] = '<span style="color:red;">LOUE</span>'
			prop['frequency'] = ''
		else:
			prop['price'] = ''
		prop['img'] = row['pics'][0].replace('/s0/','/s400/').replace('/s640/','/s400/')
		topsixdict['props'].append(prop)

		#if rowcount == _mghsettings.PPP:
			#rowcount = 0
			#propstoprocess = propstoprocess - _mghsettings.PPP
			#print propstoprocess
			#pagenext = pagecount+1
			#pageprev = pagecount-1
			#if propstoprocess < _mghsettings.PPP:
			#	pagenext = 0
			#if pageprev < 0:
			#	pageprev = 0
			#makepage(topsixdict,pageprev,pagenext,pagecount, rubrun['pagename_en'], rubrun['pagename_de'], rubrun['pagename_nl'], rubrun['pagename_fr'])
			#pagecount = pagecount + 1
			#topsixdict['props'] = []



	if len(topsixdict) > 0:
		makepage(topsixdict,pagecount-1,0,pagecount, rubrun['pagename_en'], rubrun['pagename_de'], rubrun['pagename_nl'], rubrun['pagename_fr'])
