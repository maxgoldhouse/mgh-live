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

templateLoader = jinja2.FileSystemLoader(_mghsettings.EN_TEMPLATEFOLDER)
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "topsixindex.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

db=sqlite3.connect(_mghsettings.DATAFOLDER+'mgh.db')
db.row_factory = sqlite3.Row
cursor=db.cursor()

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


cursor.execute("SELECT * FROM  mghprops WHERE  blndisplay = 1 AND blnrental = 0 AND blntopsix = 1 ORDER BY intprice ASC")
for row in cursor:
	#print('{0},{1},{2},{3},{4}'.format(row['strpropertyid'],row['strpropertyref'],row['strpropertytype'],row['intprice'],row['strlocation_detail']))
	#print getpropfirstpic(row['strpropertyref'])
	#print '/'+row['strpropertyid']+'-'+str(row['intbeds'])+' bed '+row['strpropertytype']+' in '+row['strlocation_detail']+'.html'
    propurl = '/'+str(row['intbeds'])+'-bed-'+row['strpropertytype'].replace(' ','-')+'-in-'+row['strlocation_detail'].replace(' ','-')+'-'+row['strpropertyid']+'.html'
    if row['blnrental'] == 1:
    	saleorrent = 'rent'
    else:
    	saleorrent = 'sale'
    prop = {}
    prop['propopt'] = row['strPropertyOptions']
    prop['propid'] = row['strpropertyid']
    prop['propurl'] = propurl
    prop['locationdetail']=row['strlocation_detail']
    prop['proptype']=row['strpropertytype']
    prop['saleorrent']=saleorrent
    prop['underoffersold'] = row['intunderoffersold']
    if row['intunderoffersold'] == 0:
        prop['price'] = "<span class='price_eur'>&euro;"+"{:,}".format(row['intprice'])+"</span> "
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
    else:
        prop['price'] = ''
    prop['img'] = getpropfirstpic(row['strpropertyid'])
    topsixdict['props'].append(prop)

for item in topsixdict['props']:

    for key in item:
    	print item[key]

outputText = template.render(topsixdict)
print outputText
file = open(_mghsettings.EN_SITEDIR+"index.html", "w")
file.write(outputText)
file.close()

TEMPLATE_FILE = "allpropsindex.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

cursor.execute("SELECT * FROM  mghprops WHERE  blndisplay = 1 AND blnrental = 0 ORDER BY intprice ASC")
for row in cursor:
    propurl = '/'+str(row['intbeds'])+'-bed-'+row['strpropertytype'].replace(' ','-')+'-in-'+row['strlocation_detail'].replace(' ','-')+'-'+row['strpropertyid']+'.html'
    prop = {}
    prop['description'] = removenonascci(row['strdescription'][:400])
    prop['beds'] = row['intbeds']
    prop['baths'] = row['intbaths']
    prop['propid'] = row['strpropertyid']
    prop['propref'] = row['strpropertyref']
    prop['propurl'] = propurl
    prop['locationdetail']=row['strlocation_detail']
    prop['proptype']=row['strpropertytype']
    prop['saleorrent']= 'sale'
    prop['underoffersold'] = row['intunderoffersold']
    if row['intunderoffersold'] == 0:
        prop['price'] = "<span class='price_eur'>&euro;"+"{:,}".format(row['intprice'])+"</span> "
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
    allprops['props'].append(prop)

for item in allprops['props']:
	for key in item:
		print item[key]

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
