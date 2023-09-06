#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#############################################################################
#############################################################################
#############################################################################
# pip3 install tabulate --user
#
# https://my.webrootanywhere.com/gsm.aspx#/uber/settings/apiaccess
#############################################################################
import requests
import json
import argparse
import sys, os.path
from configparser import ConfigParser
from requests.auth import HTTPBasicAuth
from tabulate import tabulate
from http.client import HTTPConnection
from datetime import date, datetime, timedelta

api_url = 'https://unityapi.webrootcloudav.com/'

def request( method='GET', resource='', params='', headers={"accept": "application/json",} ):
  url=api_url+resource
  if (args.debug):
    print(url)
    # print statements from `http.client.HTTPConnection` to console/stdout
    HTTPConnection.debuglevel = 1
  if method=='POST':
    response = requests.post(
      api_url+resource,
      headers=headers,
      data=params
    )
  elif method=='GET':
    if params:
      urlp=''
      for param in params:
        if urlp=='':
          urlp=urlp+param
        else:
          urlp=urlp+"&"+param
      url=url+"?"+urlp
    response = requests.get(
      url,
      headers=headers,
    )
  if not (args.noverbose) or (args.debug):
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=2, separators=(',', ': ')))
  return(response.json())
#############################################################################
#############################################################################
parser = argparse.ArgumentParser(description='https://github.com/osgpcq/webroot-cli-py',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--client',               default='exo',       help='Config file selection')
parser.add_argument('--active',               action='store_true', help='Choose active endpoints')
parser.add_argument('--last',                 action='store_true', help='Check not seen')
parser.add_argument('--debug',                action='store_true', help='Debug information')
parser.add_argument('--noverbose',            action='store_true', default=False, help='Verbose')
args = parser.parse_args()

config_file='./config.conf'
if os.path.isfile(config_file):
  parser = ConfigParser(interpolation=None)
  parser.read(config_file, encoding='utf-8')
  api_id = str(parser.get('webroot', 'id'))
  api_secret = str(parser.get('webroot', 'secret'))
  email = str(parser.get('webroot', 'email'))
  password = str(parser.get('webroot', 'password'))
  gsm = str(parser.get('webroot', 'key_'+args.client))
else:
  sys.exit('Configuration file not found!')

health_version=request( resource='service/api/health/version', headers={"accept": "application/json", 'Content-Type': 'application/x-www-form-urlencoded' } )
health_ping=request( resource='service/api/health/ping', headers={"accept": "application/json", 'Content-Type': 'application/x-www-form-urlencoded' } )

# [\"SkyStatus.Site\",\"SkyStatus.GSM\",\"SkyStatus.Usage\",\"SkyStatus.Reporting\",\"Console.GSM\"]"
#auth=request( resource='auth/token', method='POST', params={ 'client_id': api_id, 'client_secret': api_secret, 'username': email, 'password': password, 'grant_type': 'password', 'scope': '*' }, headers={"accept": "application/json", 'Content-Type': 'application/x-www-form-urlencoded' } )
#auth=request( resource='auth/token', method='POST', params={ 'client_id': api_id, 'client_secret': api_secret, 'username': email, 'password': password, 'grant_type': 'password', 'scope': 'skystatus.reporting' }, headers={"accept": "application/json", 'Content-Type': 'application/x-www-form-urlencoded' } )
auth=request( resource='auth/token', method='POST', params={ 'client_id': api_id, 'client_secret': api_secret, 'username': email, 'password': password, 'grant_type': 'password', 'scope': '*' }, headers={"accept": "application/json", 'Content-Type': 'application/x-www-form-urlencoded' } )

subscription=request( resource='service/api/notifications/subscriptions', headers={"accept": "application/json", 'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer '+auth['access_token']} )

status_site=request( resource='service/api/status/site/'+gsm, headers={"accept": "application/json", 'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer '+auth['access_token']} )
table = []
print('Count: '+str(status_site['Count']))
print('Date: '+str(date.today()))
for endpoint in status_site['QueryResults']:
  if ( not (args.active) ) or ((args.active) and not endpoint['Deactivated']):
    if ( not (args.last) ) or ((args.last) and ( datetime.strptime(endpoint['LastSeen'],'%Y-%m-%dT%H:%M:%S') < datetime.today()-timedelta(7) )):
      table.append([
        endpoint['Deactivated'],
        endpoint['BasicInfo']['DeviceType'],
        endpoint['OS'],
        endpoint['HostName'],
        endpoint['OSAndVersions']['CurrentUser'],
        endpoint['IPAddress'],
        endpoint['OSAndVersions']['IPV4'],
        endpoint['OSAndVersions']['MACAddress'],
        endpoint['OSAndVersions']['PrimaryBrowser'],
        endpoint['OSAndVersions']['Workgroup'],
        endpoint['OSAndVersions']['IsFirewallEnabled'],
        endpoint['ClientVersion'],
        endpoint['BasicInfo']['AttentionRequired'],
        endpoint['BasicInfo']['Infected'],
        endpoint['BasicInfo']['ActiveThreats'],
        endpoint['BasicInfo']['Managed'],
        endpoint['ExtendedInfo']['HasBeenInfected'],
        endpoint['TimesAndStats']['ThreatsRemoved'],
        endpoint['Scheduling']['ScheduledScansEnabled'],
        endpoint['LastSeen'],
        endpoint['TimesAndStats']['LastScan'],
        endpoint['TimesAndStats']['LastDeepScan'],
      ]),
print(tabulate(sorted(table), headers=['Deactivated','DeviceType','OS','HostName','CurrentUser','IPAddress','IPV4','MACAddress','PrimaryBrowser','Workgroup','IsFirewallEnabled','ClientVersion','AttentionRequired','Infected','ActiveThreats','Managed','HasBeenInfected','ThreatsRemoved','ScheduledScansEnabled','LastSeen','LastScan','LastDeepScan']))


#############################################################################
#############################################################################
#############################################################################
