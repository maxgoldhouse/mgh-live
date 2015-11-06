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

templateLoader = jinja2.FileSystemLoader(_mghsettings.NL_TEMPLATEFOLDER)
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "nl_topsixindex.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

db=sqlite3.connect(_mghsettings.DATAFOLDER+'mgh.db')
db.row_factory = sqlite3.Row
cursor=db.cursor()

picasaurlsdir = '/home/papo/mgh-admin/MyMGHProject/picasaurls/'

topsixdict = {}
allprops = {}

def removeumlauts(text):
	outchars = {u'\xb4':'&acute;',u'\u20ac':'&euro;',u'\xe1':'a',u'\xf1':'n',u'\xed':'i',u'\u2013':'',u'\xa8':'',u'\xad':'-',u'Ä':'&Auml;',u'ä':'&auml;',u'Ë':'&Euml;',u'ë':'&euml;',u'Ï':'&Iuml;',u'ï':'&iuml;',u'Ö':'&Ouml;',u'ö':'&ouml;',u'ß':'&szlig;',u'Ü':'&Uuml;',u'ü':'&uuml;'}
	for i, j in outchars.iteritems():
		text = text.replace(i, j)
	return text

def getpropfirstpic(album):
	myfile = open(picasaurlsdir+row['strpropertyid']+".pics","r")
	mylines = list(myfile)
	myfile.close()
	return mylines[0].replace('/s0/','/s400/')

topsixdict['title'] = 'Villamartin Eigendom te koop, Playa Flamenca, Cabo Roig, Guardamar del Segura, Ciudad Quesada Costa Blanca Spain'
topsixdict['keywords'] = 'Villamartin Eigendom te koop, Playa Flamenca, Cabo Roig, Guardamar del Segura and Ciudad Quesada'
topsixdict['description'] = 'Eigendom te koop Villamartin, Playa Flamenca, Cabo Roig, Los Altos, Los Balcones, Guardamar del Segura, Ciudad Quesada in Torrevieja and  Orihuela Costa areas of Southern Costa Blanca Spain'
topsixdict['props'] = []
allprops['props'] = []


cursor.execute("SELECT * FROM  mghprops WHERE  blndisplay = 1 AND blnrental = 0 AND blntopsix = 1 ORDER BY intprice ASC")
for row in cursor:
	#print('{0},{1},{2},{3},{4}'.format(row['strpropertyid'],row['strpropertyref'],row['strpropertytype'],row['intprice'],row['strlocation_detail']))
	#print getpropfirstpic(row['strpropertyref'])
	#print '/'+row['strpropertyid']+'-'+str(row['intbeds'])+' bed '+row['strpropertytype']+' in '+row['strlocation_detail']+'.html'
	nl_proptype = _mghsettings.trans_proptypes[row['strpropertytype'].lower()]['nl']
	propurl = '/'+str(row['intbeds'])+'-slaapkamer-'+nl_proptype.replace(' ','-')+'-in-'+row['strlocation_detail'].replace(' ','-')+'-'+row['strpropertyid']+'.html'
	if row['blnrental'] == 1:
		saleorrent = 'te huur'
	else:
		saleorrent = 'te koop'
	prop = {}
	prop['propopt'] = row['strPropertyOptions']
	prop['propid'] = row['strpropertyid']
	prop['propurl'] = propurl
	prop['locationdetail']=row['strlocation_detail']
	prop['proptype'] = nl_proptype
	prop['saleorrent']=saleorrent
	prop['underoffersold'] = row['intunderoffersold']
	if row['intunderoffersold'] == 0:
		prop['price'] = "&euro;"+"{:,}".format(row['intprice']).replace(',','.')
	elif row['intunderoffersold'] == 2:
		prop['price'] = 'VERKOCHT'
	else:
		prop['price'] = ''
	prop['img'] = getpropfirstpic(row['strpropertyid'])
	topsixdict['props'].append(prop)


"""for item in topsixdict['props']:
	for key in item:
		print item[key] """

outputText = template.render(topsixdict)
#print outputText
file = open(_mghsettings.NL_SITEDIR+"index.html", "w")
file.write(outputText)
file.close()

TEMPLATE_FILE = "nl_allpropsindex.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

cursor.execute("SELECT * FROM  mghprops WHERE  blndisplay = 1 AND blnrental = 0 ORDER BY intprice ASC")
for row in cursor:
    nl_proptype = _mghsettings.trans_proptypes[row['strpropertytype'].lower()]['nl']
    propurl = '/'+str(row['intbeds'])+'-slaapkamer-'+nl_proptype.replace(' ','-')+'-in-'+row['strlocation_detail'].replace(' ','-')+'-'+row['strpropertyid']+'.html'
    if row['blnrental'] == 1:
    	saleorrent = 'te huur'
    else:
    	saleorrent = 'te koop'
    prop = {}
    prop['fulldescription'] = row['strdescription_NL']
    #prop['description'] = removeumlauts(row['strdescription_NL'][:400])
    prop['description'] = row['strdescription_NL'][:400]
    if row['intbeds'] == 1:
	    slaapkamer = ' slaapkamer'
    elif row['intbeds'] > 1:
	    slaapkamer = ' slaapkamers'
    prop['beds'] = str(row['intbeds']) + slaapkamer
    if row['intbaths'] == 1:
	    badkamer = ' badkamer'
    elif row['intbaths'] > 1:
	    badkamer = ' badkamers'
    prop['baths'] = str(row['intbaths']) + badkamer
    prop['propid'] = row['strpropertyid']
    prop['propref'] = row['strpropertyref']
    prop['propurl'] = propurl
    prop['locationdetail']=row['strlocation_detail']
    prop['proptype'] = nl_proptype
    prop['saleorrent']=saleorrent
    prop['underoffersold'] = row['intunderoffersold']
    if row['intunderoffersold'] == 0:
    	prop['price'] = "<span class='price_eur'>&euro;"+"{:,}".format(row['intprice']).replace(',','.')+"</span> "
    elif row['intunderoffersold'] == 2:
    	prop['price'] = 'VERKOCHT'
    elif row['intunderoffersold'] == 3:
    	prop['price'] = '<span style="color:red;">VERHUURD</span>'
    else:
    	prop['price'] = ''
    prop['img'] = getpropfirstpic(row['strpropertyid'])
    allprops['props'].append(prop)

EllenText = ''
for item in allprops['props']:
	#for key in item:
	EllenText = EllenText + '++++++++++++++++++++++++++++++++++++\n'
	EllenText = EllenText + item['propid'] + '\n'
	EllenText = EllenText +  item['propref'] + '\n'
	EllenText = EllenText +  item['locationdetail'] + '\n'
	EllenText = EllenText +  item['proptype'] + '\n'
	EllenText = EllenText +  '>>>>>>>' + '\n'
	EllenText = EllenText +  item['fulldescription'] + '\n'
	EllenText = EllenText +  '>>>>>>>' + '\n'



outputText = template.render(allprops)
#print outputText
file = open(_mghsettings.NL_SITEDIR+"allindex.html", "w")
file.write(outputText)
file.close()

file = open(_mghsettings.NL_SITEDIR+"Ellen.txt", "w")
file.write(EllenText)
file.close()
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
