#!thisenv/bin/python

import requests
from requests.auth import HTTPBasicAuth
from pprint import pprint


url  = "http://localhost:5000/country"

url  = "http://localhost:5000/props"

# headers = { "x-api-key" : "my-api-key", "Content-Type" : "application/json" }

headers = { "Content-Type" : "application/json" }

resp =  requests.get(url)
pprint(resp)

resp =  requests.get(url, headers = headers)
pprint(resp)

url  = "http://localhost:5000/prop"

resp =  requests.post(url, json = { 'name' : 'New Name Req', 'value' : 'New Value Req' },
                           auth=HTTPBasicAuth('flaskrestuser', 'flaskrestpwd'))
pprint(resp)

url  = "http://localhost:5000/props"
resp = requests.get(url,headers=headers)
pprint(resp)

url  = "http://localhost:5000/prop"
resp =  requests.delete(url, json = { 'name' : 'New Name Req'},
                           auth=HTTPBasicAuth('flaskrestuser', 'flaskrestpwd'))
pprint(resp)

url  = "http://localhost:5000/props"
resp = requests.get(url,headers=headers)
pprint(resp)


#
# Supported resp methods / fields ...
#
#    resp.apparent_encoding  resp.cookies    resp.history               resp.iter_lines  resp.raise_for_status  resp.status_code
#    resp.close              resp.elapsed    resp.is_permanent_redirect resp.json        resp.raw               resp.text     
#    resp.connection         resp.encoding   resp.is_redirect           resp.links       resp.reason            resp.url
#    resp.content            resp.headers    resp.iter_content          resp.ok          resp.request
#
