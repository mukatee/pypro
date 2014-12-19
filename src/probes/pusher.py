__author__ = 'teemu kanstren'

import urllib.request
import json

body = {'ids': [12, 14, 50]}

myurl = "http://www.testmycode.com"
req = urllib.request.Request(myurl)
req.add_header('Content-Type', 'application/json; charset=utf-8')
jsondata = json.dumps(body)
jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
req.add_header('Content-Length', len(jsondataasbytes))
print(jsondataasbytes)
