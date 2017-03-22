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
TEMPLATE_FILE = "fr_topsixindex.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

topsixdict = {}
allprops = {}

topsixdict['title'] = 'Villamartin Propri&eacute;t&eacute; a vendre, Playa Flamenca, Cabo Roig, Guardamar del Segura, Ciudad Quesada Costa Blanca Spain'
topsixdict['keywords'] = 'Villamartin propriete a vendre, Playa Flamenca, Cabo Roig, Guardamar del Segura and Ciudad Quesada'
topsixdict['description'] = 'Propri&eacute;t&eacute; a vendre Villamartin, Playa Flamenca, Cabo Roig, Los Altos, Los Balcones, Guardamar del Segura'
topsixdict['props'] = []
allprops['props'] = []

thetopsix = _mgh_data.proplists['topsix']
for fetchprop in thetopsix:
	row = _mgh_data.props[str(fetchprop)]
	fr_proptype = _mghsettings.trans_proptypes[row['ptype'].lower()]['fr']
	propurl = '/'+str(row['beds'])+'-chambre-'+fr_proptype.replace(' ','-').replace('é','e')+'-a-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
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
	topsixdict['props'].append(prop)

### insert the accommodation offer into the position 1of the list
prop = {}
prop['proptype'] = 'mghoffer'
prop['offerHTML'] = '<div class="featured_property_wrap col-sm-4"><style>#offer{font-size:20px;} .mgh-offer{text-align:center;}</style><div class="mgh-offer"><img src="//lh3.googleusercontent.com/-GTT16P545Io/WA8sWvHiQZI/AAAAAAAAP6o/8rxFFVCigjwJ_o2_7QVO7SU-NCs_dFAHACL0B/s0-rj/150-euros.jpg" class="img-thumbnail img-circle img-responsive"><div id="offer">Nous pouvons payer<br/> votre note d’hôtel?</div><div class="col-sm-offset-1"><a href="/herbergement-gratuit.html"><button class="btn btn-success">Savoir Plus</button></a></div></div></div>'
topsixdict['props'].insert(1,prop)

outputText = template.render(topsixdict)
#print outputText
file = open(_mghsettings.FR_SITEDIR+"index.html", "w")
file.write(outputText)
file.close()

TEMPLATE_FILE = "fr_allpropsindex.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

for eachprop in _mgh_data.proplists['All']:
    row = _mgh_data.props[str(eachprop)]
    fr_proptype = _mghsettings.trans_proptypes[row['ptype'].lower()]['fr']
    propurl = '/'+str(row['beds'])+'-chambre-'+fr_proptype.replace(' ','-').replace('é','e')+'-a-'+row['location'].replace(' ','-')+'-'+row['pid']+'.html'
    if row['rental'] == 'True':
    	saleorrent = 'à loure'
    else:
    	saleorrent = 'à vendre'
    prop = {}
    prop['fulldescription'] = row['FR']
    #prop['description'] = removefrchars(row['strdescription_FR'][:400])
    if row['FR'][:400][-1] == '\xc3':
		prop['description'] = row['FR'][:399]
    else:
		prop['description'] = row['FR'][:400]
    if int(row['beds']) == 1:
		chambre = ' chambre'
    elif int(row['beds']) > 1:
		chambre = ' chambres'
    prop['beds'] = row['beds'] + chambre
    if int(row['baths']) == 1:
		bain = ' salle de bain'
    elif int(row['baths']) > 1:
		bain = ' salles de bains'
    prop['baths'] = row['baths'] + bain
    prop['pool'] = _mghsettings.trans_pooltypes[row['pool'].lower()]['fr']
    prop['propid'] = row['pid']
    prop['propref'] = row['ref']
    prop['propurl'] = propurl
    prop['town']=row['town']
    prop['province']=row['province']
    prop['locationdetail']=row['location']
    prop['proptype'] = fr_proptype
    prop['saleorrent']=saleorrent
    prop['sprice'] = row['price']
    prop['underoffersold'] = row['salestage']
    if row['salestage'] == '0':
    	prop['price'] = "<span class='price_eur'>&euro;"+"{:,}".format(int(row['price'])).replace(',','.')+"</span> "
    elif row['salestage'] == '2':
    	prop['price'] = 'VENDU'
    elif row['salestage'] == '3':
    	prop['price'] = '<span style="color:red;">LOUE</span>'
    else:
    	prop['price'] = ''
    prop['img'] = row['pics'][0].replace('/s0/','/s400/').replace('/s640/','/s400/')
    allprops['props'].append(prop)

outputText = template.render(allprops)
#print outputText
file = open(_mghsettings.FR_SITEDIR+"allindex.html", "w")
file.write(outputText)
file.close()

#Now lets make the JSON file for taffyDB
TEMPLATE_FILE = "taffyDB.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )
outputText = template.render(allprops)
file = open(_mghsettings.FR_SITEDIR+"allprops.json", "w")
file.write(outputText)
file.close()
