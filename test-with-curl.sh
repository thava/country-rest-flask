#!/bin/bash

curl  http://localhost:5000

curl  http://localhost:5000  | python -m json.tool


curl  http://localhost:5000/country 
curl  http://localhost:5000/country  | python -m json.tool

curl  http://localhost:5000/props

curl -u flaskrestuser:flaskrestpwd -H "Content-Type: application/json" \
     -X POST -d '{ "name" : "New Property" , "value" : "New Value" }'  http://localhost:5000/prop

#
# Note:  Use -H "x-api-key:my-custom-api-key" if your app needs it.
#

curl  http://localhost:5000/props

curl -u flaskrestuser:flaskrestpwd -H "Content-Type: application/json" \
     -X DELETE -d '{ "name" : "New Property" }'  http://localhost:5000/prop

curl  http://localhost:5000/props


