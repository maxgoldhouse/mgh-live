#!/usr/bin/python3
import urllib
import urllib

testfile = urllib.URLopener()
testfile.retrieve("http://mgh-props.appspot.com/pydata", "_mgh_data.py")
testfile.retrieve("http://mgh-props.appspot.com/refs", "refsearch.html")
#urllib.urlretrieve ("http://mgh-props.appspot.com/pydata", "_mgh_data.py")
#urllib.urlretrieve ("http://mgh-props.appspot.com/refs", "refsearch.html")
