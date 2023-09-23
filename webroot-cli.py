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
#############################################################################
def request( method='GET', resource='' , auth='', headers={}, params='', data='' ):
  # data:   POST, PUT, ...
  # params: GET, ...
  url=api_url+resource
  headers.update({'accept': 'application/json'})
  if (args.verbose) or (args.debug):
    print(url)
    if (args.debug):
      # print statements from `http.client.HTTPConnection` to console/stdout
      HTTPConnection.debuglevel=1
  response=requests.request(
    method,
    api_url+resource,
    auth=auth,
    headers=headers,
    params=params,
    data=data
  )
  if (args.verbose) or (args.debug):
    print('Status code: '+str(response.status_code))
  if (args.debug):
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=2, separators=(',', ': ')))
  return(response.json())
#############################################################################
def table_endpoints( status_site_f ):
  for endpoint in status_site_f['QueryResults']:
    if ( not (args.active) ) or ((args.active) and not endpoint['Deactivated']):
      if ( not (args.last) ) or ((args.last) and ( datetime.strptime(endpoint['LastSeen'],'%Y-%m-%dT%H:%M:%S') < datetime.today()-timedelta(7) )):
        table.append([
          str(endpoint['Deactivated']),
          str(endpoint['BasicInfo']['DeviceType']),
          str(endpoint['OS']),
          str(endpoint['HostName']),
          str(endpoint['OSAndVersions']['CurrentUser']),
          str(endpoint['IPAddress']),
          str(endpoint['OSAndVersions']['IPV4']),
          str(endpoint['OSAndVersions']['MACAddress']),
          str(endpoint['OSAndVersions']['PrimaryBrowser']),
          str(endpoint['OSAndVersions']['Workgroup']),
          str(endpoint['OSAndVersions']['IsFirewallEnabled']),
          str(endpoint['ClientVersion']),
          str(endpoint['BasicInfo']['AttentionRequired']),
          str(endpoint['BasicInfo']['Infected']),
          str(endpoint['BasicInfo']['ActiveThreats']),
          str(endpoint['BasicInfo']['Managed']),
          str(endpoint['ExtendedInfo']['HasBeenInfected']),
          str(endpoint['TimesAndStats']['ThreatsRemoved']),
          str(endpoint['Scheduling']['ScheduledScansEnabled']),
          str(endpoint['LastSeen']),
          str(endpoint['TimesAndStats']['LastScan']),
          str(endpoint['TimesAndStats']['LastDeepScan']),
        ]),
  return(table)
#############################################################################
#############################################################################
parser = argparse.ArgumentParser(description='https://github.com/osgpcq/webroot-cli-py',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--client',               default='exo',       help='Choose the GSM key')
parser.add_argument('--endpoints',            action='store_true', help='List endpoints')
parser.add_argument('--active',               action='store_true', help='Only active endpoints')
parser.add_argument('--last',                 action='store_true', help='Only endpoints not seen for 7 days')
parser.add_argument('--ping',                 action='store_true', help='Ping')
parser.add_argument('--version',              action='store_true', help='Version')
parser.add_argument('--subscriptions',        action='store_true', help='List subscriptions')
parser.add_argument('--noheaders',            action='store_true', help='No headers in the output')
parser.add_argument('--debug',                action='store_true', help='Debug information')
parser.add_argument('--verbose',              action='store_true', default=False, help='Verbose')
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

# scope: [\"SkyStatus.Site\",\"SkyStatus.GSM\",\"SkyStatus.Usage\",\"SkyStatus.Reporting\",\"Console.GSM\",\"Notifications.Subscriptions\"]"
authtoken=request( method='POST', resource='auth/token', headers={ 'Content-Type': 'application/x-www-form-urlencoded' }, data={ 'client_id': api_id, 'client_secret': api_secret, 'username': email, 'password': password, 'grant_type': 'password', 'scope': '*' } )

if (args.ping):
  health_ping=request( resource='service/api/health/ping', headers={ 'Content-Type': 'application/x-www-form-urlencoded' } )
if (args.version):
  health_version=request( resource='service/api/health/version', headers={ 'Content-Type': 'application/x-www-form-urlencoded' } )
if (args.subscriptions):
  subscriptions=request( resource='service/api/notifications/subscriptions', headers={ 'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer '+authtoken['access_token'] } )

if (args.endpoints):
  params = ''
  table = []
  endpoints = { 'ContinuationToken': True }
  if (args.verbose) or (args.debug):
    print('Date: '+str(date.today()))
  while endpoints['ContinuationToken']:
    endpoints=request( resource='service/api/status/site/'+gsm, headers={ 'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer '+authtoken['access_token']}, params=params )
    params = { 'Continuation': endpoints['ContinuationToken'] }
    if (args.verbose) or (args.debug):
      print('Count: '+str(endpoints['Count']))
    if (args.debug):
      print('ContinuationToken: '+str(endpoints['ContinuationToken']))
      print('ContinuationURI: '+str(endpoints['ContinuationURI']))
    table_endpoints(endpoints)
  if (args.noheaders):
    print(tabulate(sorted(table), tablefmt='plain', showindex=True))
  else:
    print(tabulate(sorted(table), tablefmt='rounded_outline', headers=['Deactivated','DeviceType','OS','HostName','CurrentUser','IPAddress','IPV4','MACAddress','PrimaryBrowser','Workgroup','IsFirewallEnabled','ClientVersion','AttentionRequired','Infected','ActiveThreats','Managed','HasBeenInfected','ThreatsRemoved','ScheduledScansEnabled','LastSeen','LastScan','LastDeepScan'], showindex=True ))
#############################################################################
#############################################################################
#############################################################################
