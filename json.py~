#!/usr/bin/env python

import json
import os
import urllib2

urltoopen = "http://localhost:9999/json/propdata"
urlfetch = urllib2.urlopen(urltoopen)
propjson = urlfetch.read()
#print propjson
prop_dict = json.loads(propjson)
print prop_dict
for prop in prop_dict:
   print prop_dict['props'][prop]['ref']
