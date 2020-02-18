#!/usr/bin/python
import urllib
urllib.urlretrieve ("http://mgh-props.appspot.com/pydata", "_mgh_data.py")
urllib.urlretrieve ("http://mgh-props.appspot.com/refs", "refsearch.html")
urllib.urlretrieve ("http://mgh-props.appspot.com/locations","distinctlocations.html")

'''
for python3
import urllib.request
urllib.request.urlretrieve('http://mgh-props.appspot.com/pydata','_mgh_data.py')
urllib.request.urlretrieve ("http://mgh-props.appspot.com/refs", "refsearch.html")
urllib.request.urlretrieve ("http://mgh-props.appspot.com/locations","distinctlocations.html")

'''
