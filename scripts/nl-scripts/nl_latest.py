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

templateLoader = jinja2.FileSystemLoader(_mghsettings.NL_TEMPLATEFOLDER)
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "nl_latest.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

thelatestdict = {}

thelatestdict['title'] = 'Ultieme Villamartin Eigendom te koop, Playa Flamenca, Cabo Roig, Guardamar del Segura, Ciudad Quesada Costa Blanca Spain'
thelatestdict['keywords'] = 'Ultieme Villamartin Eigendom te koop, Playa Flamenca, Cabo Roig, Guardamar del Segura and Ciudad Quesada'
thelatestdict['description'] = 'Ultieme Eigendom te koop Villamartin, Playa Flamenca, Cabo Roig, Los Altos, Los Balcones, Guardamar del Segura, Ciudad Quesada in Torrevieja and  Orihuela Costa areas of Southern Costa Blanca Spain'
thelatestdict['props'] = []


thelatest = _mgh_data.proplists['latest']
for fetchprop in thelatest:
	row = _mgh_data.props[str(fetchprop)]
	nl_proptype = _mghsettings.trans_proptypes[row['ptype'].lower()]['nl']
	propurl = '/'+str(row['beds'])+'-slaapkamer-'+nl_proptype.replace(' ','-')+'-in-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
	if row['rental'] == 'True':
		saleorrent = 'te huur'
	else:
		saleorrent = 'te koop'
	prop = {}
	prop['propid'] = row['pid']
	prop['propurl'] = propurl
	prop['locationdetail']=row['location']
	prop['proptype'] = nl_proptype
	prop['saleorrent']=saleorrent
	prop['underoffersold'] = row['salestage']
	if row['salestage'] == '0':
		prop['price'] = "&euro;"+"{:,}".format(int(row['price'])).replace(',','.')
	elif row['salestage'] == '2':
		prop['price'] = 'VERKOCHT'
	else:
		prop['price'] = ''
	prop['img'] = row['pics'][0].replace('/s0/','/s400/').replace('/s640/','/s400/')
	thelatestdict['props'].append(prop)



outputText = template.render(thelatestdict)
#print outputText
file = open(_mghsettings.NL_SITEDIR+"ultieme.html", "w")
file.write(outputText)
file.close()

