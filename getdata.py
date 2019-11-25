#!/usr/bin/python3
import urllib.request


    x = urllib.request.urlopen('http://mgh-props.appspot.com/pydata')
    saveFile = open('_mgh_data.py','w')
    saveFile.write(str(x.read()))
    saveFile.close()

    y = urllib.request.urlopen('http://mgh-props.appspot.com/refs')
    saveFile = open('refsearch.html','w')
    saveFile.write(str(y.read()))
    saveFile.close()
#urllib.urlretrieve ("http://mgh-props.appspot.com/pydata", "_mgh_data.py")
#urllib.urlretrieve ("http://mgh-props.appspot.com/refs", "refsearch.html")
