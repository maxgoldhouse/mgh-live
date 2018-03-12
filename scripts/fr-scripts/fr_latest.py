#!/usr/bin/env python
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

templateLoader = jinja2.FileSystemLoader(_mghsettings.FR_TEMPLATEFOLDER)
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "fr_latest.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

thelatestdict = {}


thelatestdict['title'] = 'Ultimes Villamartin Propri&eacute;t&eacute; a vendre, Playa Flamenca, Cabo Roig, Guardamar del Segura, Ciudad Quesada Costa Blanca Spain'
thelatestdict['keywords'] = 'Ultimes Villamartin propriete a vendre, Playa Flamenca, Cabo Roig, Guardamar del Segura and Ciudad Quesada'
thelatestdict['description'] = 'Ultimes Propri&eacute;t&eacute; a vendre Villamartin, Playa Flamenca, Cabo Roig, Los Altos, Los Balcones, Guardamar del Segura'
thelatestdict['props'] = []


thelatest = _mgh_data.proplists['latest']
for fetchprop in thelatest:
	row = _mgh_data.props[str(fetchprop)]
	fr_proptype = _mghsettings.trans_proptypes[row['ptype'].lower()]['fr']
	propurl = '/'+str(row['beds'])+'-chambre-'+fr_proptype.replace(' ','-').replace('é','e').replace('â','a')+'-a-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
	if row['rental'] == 'True':
		saleorrent = 'à louer'
	else:
		saleorrent = 'à vendre'
	prop = {}
	#prop['propopt'] = row['strPropertyOptions']
	prop['propid'] = row['pid']
	prop['pool'] = _mghsettings.trans_pooltypes[row['pool'].lower()]['fr']
	prop['propurl'] = propurl
	prop['locationdetail']=row['location']
	prop['proptype'] = fr_proptype
	prop['saleorrent']=saleorrent
	prop['underoffersold'] = row['salestage']
	if row['salestage'] == '0':
		prop['price'] = "&euro;"+"{:,}".format(int(row['price'])).replace(',','.')
	elif row['salestage'] == '2':
		prop['price'] = 'VENDU'
	else:
		prop['price'] = ''
	prop['img'] = row['pics'][0].replace('/s0/','/s400/').replace('/s640/','/s400/')
	thelatestdict['props'].append(prop)

outputText = template.render(thelatestdict)
#print outputText
file = open(_mghsettings.FR_SITEDIR+"ultimes.html", "w")
file.write(outputText)
file.close()

