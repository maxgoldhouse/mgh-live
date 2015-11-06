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

templateLoader = jinja2.FileSystemLoader(_mghsettings.FR_TEMPLATEFOLDER)
templateEnv = jinja2.Environment( loader=templateLoader )
TEMPLATE_FILE = "fr_topsixindex.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

db=sqlite3.connect(_mghsettings.DATAFOLDER+'mgh.db')
db.row_factory = sqlite3.Row
cursor=db.cursor()

picasaurlsdir = '/home/papo/mgh-admin/MyMGHProject/picasaurls/'

topsixdict = {}
allprops = {}

def removefrchars(text):
	outchars = {u'\u20ac':'&euro;',u'À':'&Agrave;',u'à':'&agrave;',u'Â':'&Acirc;',u'â':'&acirc;',u'Ç':'&Ccedil;',u'ç':'&ccedil;',u'È':'&Egrave;',u'è':'&egrave;',u'É':'&Eacute;',u'é':'&eacute;',u'Ê':'&Ecirc;',u'ê':'&ecirc;',u'Ô':'&Ocirc;',u'Û':'&Ucirc;',u'û':'&ucirc;'}
	for i, j in outchars.iteritems():
		text = text.replace(i, j)
	return text

def getpropfirstpic(album):
	myfile = open(picasaurlsdir+row['strpropertyid']+".pics","r")
	mylines = list(myfile)
	myfile.close()
	return mylines[0].replace('/s0/','/s400/')

topsixdict['title'] = 'Villamartin Propri&eacute;t&eacute; a vendre, Playa Flamenca, Cabo Roig, Guardamar del Segura, Ciudad Quesada Costa Blanca Spain'
topsixdict['keywords'] = 'Villamartin propriete a vendre, Playa Flamenca, Cabo Roig, Guardamar del Segura and Ciudad Quesada'
topsixdict['description'] = 'Propri&eacute;t&eacute; a vendre Villamartin, Playa Flamenca, Cabo Roig, Los Altos, Los Balcones, Guardamar del Segura'
topsixdict['props'] = []
allprops['props'] = []


cursor.execute("SELECT * FROM  mghprops WHERE  blndisplay = 1 AND blnrental = 0 AND blntopsix = 1 ORDER BY intprice ASC")
for row in cursor:
	#print('{0},{1},{2},{3},{4}'.format(row['strpropertyid'],row['strpropertyref'],row['strpropertytype'],row['intprice'],row['strlocation_detail']))
	#print getpropfirstpic(row['strpropertyref'])
	#print '/'+row['strpropertyid']+'-'+str(row['intbeds'])+' bed '+row['strpropertytype']+' in '+row['strlocation_detail']+'.html'
	fr_proptype = _mghsettings.trans_proptypes[row['strpropertytype'].lower()]['fr']
	propurl = '/'+str(row['intbeds'])+'-chambre-'+fr_proptype.replace(' ','-')+'-a-'+row['strlocation_detail'].replace(' ','-')+'-'+row['strpropertyid']+'.html'
	if row['blnrental'] == 1:
		saleorrent = 'à louer'
	else:
		saleorrent = 'à vendre'
	prop = {}
	prop['propopt'] = row['strPropertyOptions']
	prop['propid'] = row['strpropertyid']
	prop['propurl'] = propurl
	prop['locationdetail']=row['strlocation_detail']
	prop['proptype'] = fr_proptype
	prop['saleorrent']=saleorrent
	prop['underoffersold'] = row['intunderoffersold']
	if row['intunderoffersold'] == 0:
		prop['price'] = "&euro;"+"{:,}".format(row['intprice']).replace(',','.')
	elif row['intunderoffersold'] == 2:
		prop['price'] = 'VENDU'
	else:
		prop['price'] = ''
	prop['img'] = getpropfirstpic(row['strpropertyid'])
	topsixdict['props'].append(prop)

"""for item in topsixdict['props']:
	for key in item:
		print item[key] """

outputText = template.render(topsixdict)
#print outputText
file = open(_mghsettings.FR_SITEDIR+"index.html", "w")
file.write(outputText)
file.close()

TEMPLATE_FILE = "fr_allpropsindex.jinja"

template = templateEnv.get_template( TEMPLATE_FILE )

cursor.execute("SELECT * FROM  mghprops WHERE  blndisplay = 1 AND blnrental = 0 ORDER BY intprice ASC")
for row in cursor:
    fr_proptype = _mghsettings.trans_proptypes[row['strpropertytype'].lower()]['fr']
    propurl = '/'+str(row['intbeds'])+'-chambre-'+fr_proptype.replace(' ','-')+'-a-'+row['strlocation_detail'].replace(' ','-')+'-'+row['strpropertyid']+'.html'
    if row['blnrental'] == 1:
    	saleorrent = 'à loure'
    else:
    	saleorrent = 'à vendre'
    prop = {}
    prop['fulldescription'] = row['strdescription_FR']
    #prop['description'] = removefrchars(row['strdescription_FR'][:400])
    prop['description'] = row['strdescription_FR'][:400]
    if row['intbeds'] == 1:
		chambre = ' chambre'
    elif row['intbeds'] > 1:
		chambre = ' chambres'
    prop['beds'] = str(row['intbeds']) + chambre
    if row['intbaths'] == 1:
		bain = ' salle de bain'
    elif row['intbaths'] > 1:
		bain = ' salles de bains'
    prop['baths'] = str(row['intbaths']) + bain
    prop['propid'] = row['strpropertyid']
    prop['propref'] = row['strpropertyref']
    prop['propurl'] = propurl
    prop['locationdetail']=row['strlocation_detail']
    prop['proptype'] = fr_proptype
    prop['saleorrent']=saleorrent
    prop['underoffersold'] = row['intunderoffersold']
    if row['intunderoffersold'] == 0:
    	prop['price'] = "<span class='price_eur'>&euro;"+"{:,}".format(row['intprice']).replace(',','.')+"</span> "
    elif row['intunderoffersold'] == 2:
    	prop['price'] = 'VENDU'
    elif row['intunderoffersold'] == 3:
    	prop['price'] = '<span style="color:red;">LOUE</span>'
    else:
    	prop['price'] = ''
    prop['img'] = getpropfirstpic(row['strpropertyid'])
    allprops['props'].append(prop)


'''    for item in allprops['props']:
	   #for key in item:
		   print '++++++++++++++++++++++++++++++++++++'
		   print item['propid']
		   print item['propref']
		   print item['locationdetail']
		   print item['proptype']
		   print '>>>>>>>'
		   print item['fulldescription']
		   print '>>>>>>>'
		   print ''
'''
outputText = template.render(allprops)
#print outputText
file = open(_mghsettings.FR_SITEDIR+"allindex.html", "w")
file.write(outputText)
file.close()
