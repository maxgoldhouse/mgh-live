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
TEMPLATE_FILE = "nl_topsixindex.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

topsixdict = {}
allprops = {}

topsixdict['title'] = 'Villamartin Eigendom te koop, Playa Flamenca, Cabo Roig, Guardamar del Segura, Ciudad Quesada Costa Blanca Spain'
topsixdict['keywords'] = 'Villamartin Eigendom te koop, Playa Flamenca, Cabo Roig, Guardamar del Segura and Ciudad Quesada'
topsixdict['description'] = 'Eigendom te koop Villamartin, Playa Flamenca, Cabo Roig, Los Altos, Los Balcones, Guardamar del Segura, Ciudad Quesada in Torrevieja and  Orihuela Costa areas of Southern Costa Blanca Spain'
topsixdict['props'] = []
allprops['props'] = []

thetopsix = _mgh_data.proplists['topsix']
for fetchprop in thetopsix:
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
	topsixdict['props'].append(prop)

### insert the accommodation offer into the position 1of the list
prop = {}
prop['proptype'] = 'mghoffer'
prop['offerHTML'] = '<div class="featured_property_wrap col-sm-4"><style>#offer{font-size:20px;} .mgh-offer{text-align:center;}</style><div class="mgh-offer"><img src="//lh3.googleusercontent.com/-GTT16P545Io/WA8sWvHiQZI/AAAAAAAAP6o/8rxFFVCigjwJ_o2_7QVO7SU-NCs_dFAHACL0B/s0-rj/150-euros.jpg" class="img-thumbnail img-circle img-responsive"><div id="offer">Kunnen wij uw <br/>hotelrekening betalen?</div><div class="col-sm-offset-1"><a href="/accomodatie.html"><button class="btn btn-success">Vertel me meer</button></a></div></div></div>'
topsixdict['props'].insert(1,prop)


outputText = template.render(topsixdict)
#print outputText
file = open(_mghsettings.NL_SITEDIR+"index.html", "w")
file.write(outputText)
file.close()

TEMPLATE_FILE = "nl_allpropsindex.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

for eachprop in _mgh_data.proplists['All']:
    row = _mgh_data.props[str(eachprop)]
    nl_proptype = _mghsettings.trans_proptypes[row['ptype'].lower()]['nl']
    propurl = '/'+str(row['beds'])+'-slaapkamer-'+nl_proptype.replace(' ','-')+'-in-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
    if row['rental'] == 'True':
    	saleorrent = 'te huur'
    else:
    	saleorrent = 'te koop'
    prop = {}
    if row['NL'][:400][-1] == '\xc3':
		prop['description'] = row['NL'][:399]
    else:
		prop['description'] = row['NL'][:400]
    if int(row['beds']) == 1:
	    slaapkamer = ' slaapkamer'
    elif int(row['beds']) > 1:
	    slaapkamer = ' slaapkamers'
    prop['beds'] = row['beds'] + slaapkamer
    if int(row['baths']) == 1:
	    badkamer = ' badkamer'
    elif int(row['baths']) > 1:
	    badkamer = ' badkamers'
    prop['baths'] = row['baths'] + badkamer
    prop['propid'] = row['pid']
    prop['propref'] = row['ref']
    prop['propurl'] = propurl
    prop['locationdetail']=row['location']
    prop['proptype'] = nl_proptype
    prop['saleorrent']=saleorrent
    prop['underoffersold'] = row['salestage']
    if row['salestage'] == '0':
    	prop['price'] = "<span class='price_eur'>&euro;"+"{:,}".format(int(row['price'])).replace(',','.')+"</span> "
    elif row['salestage'] == '2':
    	prop['price'] = 'VERKOCHT'
    elif row['salestage'] == '3':
    	prop['price'] = '<span style="color:red;">VERHUURD</span>'
    else:
    	prop['price'] = ''
    prop['img'] = row['pics'][0].replace('/s0/','/s400/').replace('/s640/','/s400/')
    allprops['props'].append(prop)

outputText = template.render(allprops)
#print outputText
file = open(_mghsettings.NL_SITEDIR+"allindex.html", "w")
file.write(outputText)
file.close()
