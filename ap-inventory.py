#!/usr/bin/python3 

# Upload Inventory to Aruba Central from a CSV file. 
# (c) 2022 Ian Beyer, ian.beyer@hpe.com

# Import Aruba Central Base
from pycentral.base import ArubaCentralBase
import pprint
import csv
import yaml
import argparse
import json
import os
from pathlib import Path

pp = pprint.PrettyPrinter(indent=3)

data=[]

datafile='datafile.csv'
cli=argparse.ArgumentParser(description='Create a list of sites in Aruba Central from a CSV file.')

cli.add_argument("-t", "--token", required=False, help='Downloaded token file (JSON)', default='humana-ian.json')
cli.add_argument("-i", "--input", required=False, help='Input CSV File', default=datafile)

args = vars(cli.parse_args())

credsfile = args['token']
credspath = Path(credsfile)
if credspath.is_file() == False:
    print("Credentials file "+credsfile+" not found. Ignoring.")
else:
    with open(credsfile, 'r') as creds:
        target=json.load(creds)
    creds.close()

data=[]
with open(args['input'], 'r') as csvfile:
        reader = csv.DictReader(csvfile, dialect=csv.excel)
        for row in reader:
            values = {
            'serial':row['Serial'], 
             'mac':row['MAC Address']
            }
            data.append(values)
pp.pprint(data)

csvfile.close()

# Create an instance of ArubaCentralBase using API access token
# or API Gateway credentials.
central_info = {
    "base_url": "https://apigw-uswest4.central.arubanetworks.com/",
    "token": {
        "access_token": target['access_token']
    }
}
central = ArubaCentralBase(central_info=central_info,
                           ssl_verify=True)
for ap in data:

    req_body=[
      {
        "mac": ap['mac'],
        "serial": ap['serial']
      }
    ]

    apiPath = "/platform/device_inventory/v1/devices"
    apiMethod = "POST"
    apiParams = {
        "limit": 20,
        "offset": 0
    }
    base_resp = central.command(apiMethod=apiMethod,
                                apiPath=apiPath,
                                apiData=req_body,
                                apiParams=apiParams)
    pp.pprint(base_resp)

exit()