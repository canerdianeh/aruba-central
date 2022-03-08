#!/usr/bin/python3 

# Import Aruba Central Base
from pycentral.base import ArubaCentralBase
import pprint
import csv
import yaml
import argparse
import json

pp = pprint.PrettyPrinter(indent=3)

data=[]

datafile='datafile.csv'
cli=argparse.ArgumentParser(description='Create a list of sites in Aruba Central from a CSV file.')

cli.add_argument("-t", "--token", required=False, help='Downloaded token file (JSON)', default='token.json')
cli.add_argument("-i", "--input", required=False, help='Input CSV File', default=defaultfile)

args = vars(cli.parse_args())

with open(args['input'], 'r') as csvfile:
    reader = csv.DictReader(csvfile, dialect=csv.excel)
    for row in reader:
        values = {
        'name':row['name'], 
        'lat':row['latitude'], 
        'long':row['longitude']
        }
        if 'id' in row.keys() :
            values['id']=row['id']
        else: 
            values['id']= None
        if 'status' in row.keys() :
            values['status']=row['status']
        else:
            values['status']= None
                    
        data.append(values)
csvfile.close()

credsfile = args['credentials']
credspath = Path(credsfile)
if credspath.is_file() == False:
    print("Credentials file "+credsfile+" not found. Ignoring.")
else:
    with open(credsfile, 'r') as creds:
        target=json.load(creds)
    creds.close()


# Create an instance of ArubaCentralBase using API access token
# or API Gateway credentials.
central_info = {
    "base_url": "https://apigw-uswest4.central.arubanetworks.com/",
    "token": {
        "access_token": target['access_token']
    }
}

ssl_verify = True
central = ArubaCentralBase(central_info=central_info,
                           token_store=None,
                           ssl_verify=ssl_verify)

# Sample API call using Configuration module `pycentral.configuration`
from pycentral.monitoring import Sites

# Get groups max limit 20, apply offset and fetch other groups in loop
runner = Sites()

for site in data:
    if site['id'] != None:

        module_resp = runner.create_site(central,site['name'],geolocation={"latitude":site['lat'],"longitude":site['long']})

        if module_resp['code'] == 200 :
            siteId=module_resp['msg']['site_id']
            print("Created Successfully created side ID "+str(siteId)+" for "+module_resp['msg']['site_name'])
            site['id']=siteId
            site['status']='CREATED'

        else:
            print("There was an error "+str(module_resp['code'])+" ("+module_resp['msg']['description']+") while attempting to create site "+state['site'])



with open(args['input'], 'w') as csvfile:
    write=csv.writer(csvfile)
    columns=['name','latitude','longitude';'id','status']
    write.writerow(columns)
    for site in data:
        datarow=[]
        for c in columns:
            row.append(site[c])
        write.writerow(datarow)

csvfile.close()

