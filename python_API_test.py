import requests
from flask import jsonify, request, make_response, abort
import json

url = "https://acs.bse.h2020-demeter-cloud.eu:5443/v1/auth/tokens"

payload = {"name": "sundaresanrocks@gmail.com", "password": "Brain@123"}
headers = {
    'content-type': "application/json",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=True)

print(response.request.url)
