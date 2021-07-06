#!/usr/bin/python
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

templateLoader = jinja2.FileSystemLoader(_mghsettings.NEWEN_TEMPLATEFOLDER)
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
	return mylines[0].replace('/s0/','/s400/').replace('/s640/','/s400/')

topsixdict['title'] = 'Costa Blanca Property for Sale, Villamartin, Torrevieja, Orihuela, Orihuela Costa, Playa Flamenca, Cabo Roig, Guardamar del Segura, Ciudad Quesada'
topsixdict['keywords'] = 'Villamartin Property for sale, Playa Flamenca, Cabo Roig, Guardamar del Segura and Ciudad Quesada'
topsixdict['description'] = 'Property for sale in the Costa Blanca Alicante and Costa Calida Murcia. Apartments, Townhouses and Villas in Orihuella, Torrevieja,  Playa Flamenca, Cabo Roig, Guardamar del Segura, Ciudad Quesada'
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
    prop['ref'] = row['ref']
    prop['offplan'] = row['offplan']
    prop['propurl'] = propurl
    prop['locationdetail']=row['location']
    prop['proptype']=row['ptype']
    prop['saleorrent']=saleorrent
    prop['underoffersold'] = row['salestage']
    prop['beds'] = row['beds']
    prop['baths'] = row['baths']
    if row['salestage'] == '0':
        prop['price'] = "<span class='price_eur'>&euro;"+"{:,}".format(int(row['price']))+"</span> "
    elif row['salestage'] == '2':
        prop['price'] = 'SOLD'
    else:
        prop['price'] = ''
    print 'prop processing '+prop['propid']
    prop['img'] = row['pics'][0].replace('/s0/','/w240-e30-v2/').replace('/s640/','/w240-e30-v2/').replace('=s640','=w240').replace('=w640','=w240')
    topsixdict['props'].append(prop)
'''
for item in topsixdict['props']:
    for key in item:
    	print item[key]
'''
### ADD AN OFFER TO THE TOP 6-9 AREA
#prop = {}
#prop['proptype'] = 'mghoffer'
#prop['offerHTML'] = '<div class="featured_property_wrap col-sm-4"><style>#offer{font-size:20px;} .mgh-offer{text-align:center;}</style><div class="mgh-offer"><img src="//lh3.googleusercontent.com/-GTT16P545Io/WA8sWvHiQZI/AAAAAAAAP6o/8rxFFVCigjwJ_o2_7QVO7SU-NCs_dFAHACL0B/s240-rj-e30/150-euros.jpg" class="img-thumbnail img-circle img-responsive"><div id="offer">COULD WE PAY<br> YOUR HOTEL BILL?</div><div class="col-sm-offset-1"><a href="/offers.html"><button class="btn btn-success">Tell me more</button></a></div></div></div>'
#topsixdict['props'].insert(1,prop)

outputText = template.render(topsixdict)
#print outputText
file = open(_mghsettings.NEWEN_SITEDIR+"index.html", "w")
file.write(outputText)
file.close()

TEMPLATE_FILE = "allpropsindex.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

for eachprop in _mgh_data.proplists['All']:
    row = _mgh_data.props[str(eachprop)]
    propurl = '/'+str(row['beds'])+'-bed-'+row['ptype'].replace(' ','-')+'-in-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
    prop = {}

    if row['offplan'] == 'True':
        prop['offeris'] = 'new'
    elif row['rental'] == 'True':
        prop['offeris'] = 'rental'
    else:
        prop['offeris'] ='resale'

    prop['description'] = row['description'][:420]
    prop['offplan'] = row['offplan']
    prop['beds'] = row['beds']
    prop['baths'] = row['baths']
    prop['pool'] = row['pool']
    if prop['pool'] != 'No':
        prop['haspool'] = 'Yes'
    else:
        prop['haspool'] = 'No'    
    prop['propid'] = row['pid']
    prop['propref'] = row['ref']
    prop['propurl'] = propurl
    prop['town'] = row['town']
    prop['province'] = row['province']
    prop['locationdetail']=row['location']
    prop['uniproptype'] = row['ptype']    
    prop['proptype']=row['ptype']
    prop['saleorrent']= 'sale'
    prop['underoffersold'] = row['salestage']
    prop['sprice'] = row['price']
    
    if row['salestage'] == '0' or row['salestage'] == '10':
        prop['price'] = "<span class='price_eur'>&euro;"+"{:,}".format(int(row['price']))+"</span> "
        prop['enprice'] = "{:,}".format(int(row['price']))
    elif row['salestage'] == '2':
        prop['price'] = 'SOLD'
        prop['enprice'] = 'SOLD'
    elif row['salestage'] == '3':
    	prop['price'] = ''
    print 'allprops prop processing '+prop['propid']
    prop['img'] = row['pics'][0].replace('/s0/','/w240-e30-v2/').replace('/s640/','/w240-e30-v2/').replace('=s640','=w240').replace('=w640','=w300')
    allprops['props'].append(prop)
'''
for item in allprops['props']:
	for key in item:
		print item[key]
'''
outputText = template.render(allprops)
#print outputText
file = open(_mghsettings.NEWEN_SITEDIR+"allindex.html", "w")
file.write(outputText)
file.close()

#Now lets make the JSON file for taffyDB
TEMPLATE_FILE = "taffyDB.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )
outputText = template.render(allprops)
file = open(_mghsettings.NEWEN_SITEDIR+"allprops.json", "w")
file.write(outputText)
file.close()

#Now lets make the search.html file
TEMPLATE_FILE = "search.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )
outputText = template.render()
file = open(_mghsettings.NEWEN_SITEDIR+"search.html", "w")
file.write(outputText)
file.close()

#Now lets make the politique-de-confidentialite.html file
TEMPLATE_FILE = "privacy-policy.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )
outputText = template.render(deurl=_mghsettings.NEWDE_URL, enurl=_mghsettings.NEWEN_URL, frurl=_mghsettings.NEWFR_URL, nlurl=_mghsettings.NEWNL_URL)
file = open(_mghsettings.NEWFR_SITEDIR+"privacy-policy.html", "w")
file.write(outputText)
file.close()

#Now lets make the politique-des-cookies.html file
TEMPLATE_FILE = "cookie-policy.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )
outputText = template.render(deurl=_mghsettings.NEWDE_URL, enurl=_mghsettings.NEWEN_URL, frurl=_mghsettings.NEWFR_URL, nlurl=_mghsettings.NEWNL_URL)
file = open(_mghsettings.NEWFR_SITEDIR+"cookie-policy.html", "w")
file.write(outputText)
file.close()

#Now lets make the achat-le-processus.html file
TEMPLATE_FILE = "buying-process.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )
outputText = template.render(deurl=_mghsettings.NEWDE_URL, enurl=_mghsettings.NEWEN_URL, frurl=_mghsettings.NEWFR_URL, nlurl=_mghsettings.NEWNL_URL)
file = open(_mghsettings.NEWFR_SITEDIR+"buying-process.html", "w")
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
