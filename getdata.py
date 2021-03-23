#!/usr/bin/python
import urllib

### urllib.urlretrieve ("http://mgh-props.appspot.com/pydata", "_mgh_data.py")
### f = open('_mgh_data.py')
### line = f.readline()
### f.close()
### if line != '# -*- coding: utf-8 -*-\n':
###     urllib.urlretrieve ("http://mgh-props.appspot.com/pydata", "_mgh_data.py")

urllib.urlretrieve("https://storage.googleapis.com/mgh-props.appspot.com/mgh-data/_mgh_python.py","_mgh_data.py")

    
urllib.urlretrieve ("http://mgh-props.appspot.com/refs", "refsearch.html")
#urllib.urlretrieve ("http://mgh-props.appspot.com/getgroupedlocations","distinctlocations.html")

#urllib.urlretrieve ("http://mgh-props.appspot.com/getdistinctlocations","distinctlocations.html")

'''
for python3
import urllib.request
urllib.request.urlretrieve('http://mgh-props.appspot.com/pydata','_mgh_data.py')
urllib.request.urlretrieve ("http://mgh-props.appspot.com/refs", "refsearch.html")
urllib.request.urlretrieve ("http://mgh-props.appspot.com/locations","distinctlocations.html")

'''

