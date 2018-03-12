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
TEMPLATE_FILE = "de_latest.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

thelatestdict = {}
allprops = {}

thelatestdict['title'] = 'Neueste Villamartin Immobilien zu verkaufen, Playa Flamenca, Cabo Roig, Guardamar del Segura, Ciudad Quesada Costa Blanca Spain'
thelatestdict['keywords'] = 'Neueste Villamartin Immobilien zu verkaufen, Playa Flamenca, Cabo Roig, Guardamar del Segura and Ciudad Quesada'
thelatestdict['description'] = 'Neueste Immobilien zu verkaufen in Villamartin, Playa Flamenca, Cabo Roig, Los Altos, Los Balcones, Guardamar del Segura, Ciudad Quesada in Torrevieja and  Orihuela Costa areas of Southern Costa Blanca Spain'
thelatestdict['props'] = []
allprops['props'] = []


thelatest = _mgh_data.proplists['latest']
for fetchprop in thelatest:
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
	prop['img'] = row['pics'][0].replace('/s0/','/w400/').replace('/s640/','/w400/').replace('=s640','=w400')
	thelatestdict['props'].append(prop)

outputText = template.render(thelatestdict)
#print outputText
file = open(_mghsettings.DE_SITEDIR+"neueste.html", "w")
file.write(outputText)
file.close()

