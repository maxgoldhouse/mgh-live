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

templateLoader = jinja2.FileSystemLoader(_mghsettings.NEWNL_TEMPLATEFOLDER)
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "latest.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

thelatestdict = {}

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

thelatestdict['title'] = 'Villamartin Property for Sale, Playa Flamenca, Cabo Roig, Guardamar del Segura, Ciudad Quesada Costa Blanca Spain'
thelatestdict['keywords'] = 'Villamartin Property for sale, Playa Flamenca, Cabo Roig, Guardamar del Segura and Ciudad Quesada'
thelatestdict['description'] = 'Property for sale in Villamartin, Playa Flamenca, Cabo Roig, Los Altos, Los Balcones, Guardamar del Segura, Ciudad Quesada in Torrevieja and  Orihuela Costa areas of Southern Costa Blanca Spain'
thelatestdict['props'] = []

thelatest = _mgh_data.proplists['latest']
for fetchprop in thelatest:
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
    prop['beds'] = row['beds']
    prop['baths'] = row['baths']
    if row['salestage'] == '0':
        prop['price'] = "<span class='price_eur'>&euro;"+"{:,}".format(int(row['price']))+"</span> "
    elif row['salestage'] == '2':
        prop['price'] = 'SOLD'
    else:
        prop['price'] = ''
    prop['img'] = row['pics'][0].replace('/s0/','/w240-e30-v2/').replace('/s640/','/w240-e30-v2/').replace('=s640','=w240')
    thelatestdict['props'].append(prop)
'''
for item in thelatestdict['props']:
    for key in item:
    	print item[key]
'''
outputText = template.render(thelatestdict)
#print outputText
file = open(_mghsettings.NEWNL_SITEDIR+"latest.html", "w")
file.write(outputText)
file.close()

