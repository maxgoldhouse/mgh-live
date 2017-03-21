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

templateLoader = jinja2.FileSystemLoader(_mghsettings.DE_TEMPLATEFOLDER)
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "de_topsixindex.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

topsixdict = {}
allprops = {}

topsixdict['title'] = 'Villamartin Immobilien zu verkaufen, Playa Flamenca, Cabo Roig, Guardamar del Segura, Ciudad Quesada Costa Blanca Spain'
topsixdict['keywords'] = 'Villamartin Immobilien zu verkaufen, Playa Flamenca, Cabo Roig, Guardamar del Segura and Ciudad Quesada'
topsixdict['description'] = 'Immobilien zu verkaufen in Villamartin, Playa Flamenca, Cabo Roig, Los Altos, Los Balcones, Guardamar del Segura, Ciudad Quesada in Torrevieja and  Orihuela Costa areas of Southern Costa Blanca Spain'
topsixdict['props'] = []
allprops['props'] = []


thetopsix = _mgh_data.proplists['topsix']
for fetchprop in thetopsix:
	row = _mgh_data.props[str(fetchprop)]
	de_proptype = _mghsettings.trans_proptypes[row['ptype'].lower()]['de']
	propurl = '/'+str(row['beds'])+'-bad-'+de_proptype.replace(' ','-')+'-in-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
	if row['rental'] == 'True':
		saleorrent = 'zu vermieten'
	else:
		saleorrent = 'zu verkaufen'
	prop = {}
	#prop['propopt'] = row['strPropertyOptions']
	prop['propid'] = row['pid']
	prop['propurl'] = propurl
	prop['locationdetail']=row['location']
	prop['proptype'] = de_proptype
	prop['saleorrent']=saleorrent
	prop['underoffersold'] = row['salestage']
	if row['salestage'] == '0':
		prop['price'] = "&euro;"+"{:,}".format(int(row['price']))
	elif row['salestage'] == '2':
		prop['price'] = 'verkauft'
	else:
		prop['price'] = ''
	prop['img'] = row['pics'][0].replace('/s0/','/s400/').replace('/s640/','/s400/')
	topsixdict['props'].append(prop)

#for item in topsixdict['props']:
	#for key in item:
		#print item[key]

outputText = template.render(topsixdict)
#print outputText
file = open(_mghsettings.DE_SITEDIR+"index.html", "w")
file.write(outputText)
file.close()

TEMPLATE_FILE = "de_allpropsindex.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

for eachprop in _mgh_data.proplists['All']:
    row = _mgh_data.props[str(eachprop)]
    de_proptype = _mghsettings.trans_proptypes[row['ptype'].lower()]['de']
    propurl = '/'+str(row['beds'])+'-bad-'+de_proptype.replace(' ','-').replace('&auml;','a')+'-in-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'

    if row['rental'] == 'True':
    	saleorrent = 'zu vermieten'
    else:
    	saleorrent = 'zu verkaufen'
    prop = {}

    if row['DE'][:400][-1] == '\xc3':
		prop['description'] = row['DE'][:399]
    else:
		prop['description'] = row['DE'][:400]
    prop['beds'] = row['beds']
    prop['baths'] = row['baths']
	prop['pool'] = _mghsettings.trans_pooltypes[row['pool'].lower()]['fr']
    prop['propid'] = row['pid']
    prop['propref'] = row['ref']
    prop['propurl'] = propurl
	prop['town']=row['town']
	prop['province']=row['province']
    prop['locationdetail']=row['location']
    prop['proptype'] = de_proptype
    prop['saleorrent']=saleorrent
    prop['underoffersold'] = row['salestage']
    if row['salestage'] == '0':
    	prop['price'] = "<span class='price_eur'>&euro;"+"{:,}".format(int(row['price']))+"</span> "
    elif row['salestage'] == '2':
    	prop['price'] = 'verkauft'
    elif row['salestage'] == '3':
    	prop['price'] = '<span style="color:red;">VERMIETET</span>'
    else:
    	prop['price'] = ''
    prop['img'] = row['pics'][0].replace('/s0/','/s400/').replace('/s640/','/s400/')
    allprops['props'].append(prop)



outputText = template.render(allprops)
#print outputText
file = open(_mghsettings.DE_SITEDIR+"allindex.html", "w")
file.write(outputText)
file.close()

#Now lets make the JSON file for taffyDB
TEMPLATE_FILE = "taffyDB.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )
outputText = template.render(allprops)
file = open(_mghsettings.DE_SITEDIR+"allprops.json", "w")
file.write(outputText)
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
