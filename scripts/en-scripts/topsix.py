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
TEMPLATE_FILE = "topsixindex.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

topsixdict = {}
allprops = {}

def removenonascci(text):
    outchars = {u'\xb4':'&acute;',u'\u20ac':'&euro;',u'\xe1':'a',u'\xf1':'n',u'\xed':'i',u'\u2013':'',u'\xa8':'',u'\xad':'-'}
    for i, j in outchars.iteritems():
        text = text.replace(i, j)
    return text

def getpropfirstpic(album):
	myfile = open(_mghsettings.PICFOLDER+row['strpropertyid']+".pics","r")
	mylines = list(myfile)
	myfile.close()
	return mylines[0].replace('/s0/','/s400/')

topsixdict['title'] = 'Villamartin Property for Sale, Playa Flamenca, Cabo Roig, Guardamar del Segura, Ciudad Quesada Costa Blanca Spain'
topsixdict['keywords'] = 'Villamartin Property for sale, Playa Flamenca, Cabo Roig, Guardamar del Segura and Ciudad Quesada'
topsixdict['description'] = 'Property for sale in Villamartin, Playa Flamenca, Cabo Roig, Los Altos, Los Balcones, Guardamar del Segura, Ciudad Quesada in Torrevieja and  Orihuela Costa areas of Southern Costa Blanca Spain'
topsixdict['props'] = []
allprops['props'] = []
thetopsix = _mgh_data.proplists['topsix']
for fetchprop in thetopsix:
    row = _mgh_data.props[str(fetchprop)]
    propurl = '/'+str(row['beds'])+'-bed-'+row['ptype'].replace(' ','-')+'-in-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
    if row['rental'] == 'True':
    	saleorrent = 'rent'
    else:
    	saleorrent = 'sale'
    prop = {}
    #prop['propopt'] = row['strPropertyOptions']
    prop['propid'] = row['pid']
    prop['propurl'] = propurl
    prop['locationdetail']=row['location']
    prop['proptype']=row['ptype']
    prop['saleorrent']=saleorrent
    prop['underoffersold'] = row['salestage']
    if row['salestage'] == '0':
        prop['price'] = "<span class='price_eur'>&euro;"+"{:,}".format(int(row['price']))+"</span> "
    elif row['salestage'] == '2':
        prop['price'] = 'SOLD'
    else:
        prop['price'] = ''
    prop['img'] = row['pics'][0].replace('s0','s400')
    topsixdict['props'].append(prop)
'''
for item in topsixdict['props']:
    for key in item:
    	print item[key]
'''
outputText = template.render(topsixdict)
#print outputText
file = open(_mghsettings.EN_SITEDIR+"index.html", "w")
file.write(outputText)
file.close()

TEMPLATE_FILE = "allpropsindex.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

for eachprop in _mgh_data.proplists['All']:
    row = _mgh_data.props[str(eachprop)]
    propurl = '/'+str(row['beds'])+'-bed-'+row['ptype'].replace(' ','-')+'-in-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
    prop = {}
    prop['description'] = row['description'][:400]
    prop['beds'] = row['beds']
    prop['baths'] = row['baths']
    prop['propid'] = row['pid']
    prop['propref'] = row['ref']
    prop['propurl'] = propurl
    prop['locationdetail']=row['location']
    prop['proptype']=row['ptype']
    prop['saleorrent']= 'sale'
    prop['underoffersold'] = row['salestage']
    if row['salestage'] == '0':
        prop['price'] = "<span class='price_eur'>&euro;"+"{:,}".format(int(row['price']))+"</span> "
    elif row['salestage'] == '2':
        prop['price'] = 'SOLD'
    elif row['salestage'] == '3':
        prop['price'] = '<span style="color:red;">RENTED</span>'
        prop['frequency']= ''
    else:
    	prop['price'] = ''
    prop['img'] = row['pics'][0].replace('s0','s400')
    allprops['props'].append(prop)
'''
for item in allprops['props']:
	for key in item:
		print item[key]
'''
outputText = template.render(allprops)
#print outputText
file = open(_mghsettings.EN_SITEDIR+"allindex.html", "w")
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
