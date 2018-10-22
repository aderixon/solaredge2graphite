#!/usr/bin/env python3
#
# Script:	solaredge2graphite.py
#
# Description:	Grab PV lifetime energy & current power output from
#               SolarEdge portal, send to Graphite
#
# Requires:	Solaredge API key & site ID; see libraries below
#
# Author:	Ade Rixon
#
# History:
#	201181019 Created - ajr
#

import solaredge
import graphyte
import json
import time
import argparse
import sys

# defaults; set these or use the command line options to override
graphite_host = 'graphite'
graphite_port = 2003
graphite_pre = 'solar.pv'
apikey = 'SOLAREDGE_API_KEY'
site_id = 'XXXXXX'
time_pattern = '%Y-%m-%d %H:%M:%S'

parser = argparse.ArgumentParser(description='Reads current & total output from SolarEdge portal and submits to Graphite')
parser.add_argument('-a', '--apikey', dest='apikey', default=None, help='SolarEdge API key')
parser.add_argument('-s', '--site', dest='site_id', default=None, help='SolarEdge site ID')
parser.add_argument('-g', '--graphitehost', dest='graphite_host', default=None, help='Graphite hostname')
parser.add_argument('-p', '--graphiteprefix', dest='graphite_pre', default=None, help='Graphite prefix')
parser.add_argument('--graphiteport', dest='graphite_port', default=None, help='Graphite line receiver port')
parser.add_argument('-n', '--null', action='store_true', default=False, help='no action (send zero)')
parser.add_argument('-d', '--debug', action='store_true', default=False, help='debug (print metrics only)')
args = parser.parse_args()

if args.graphite_host:
    graphite_host = args.graphite_host
if args.graphite_pre:
    graphite_pre = args.graphite_pre
if args.graphite_port:
    graphite_port = args.graphite_port
if args.apikey:
    apikey = args.apikey
if args.site_id:
    site_id = args.site_id

r = None
if args.null:
    timestamp = int(round(time.time()))
    energy = float('nan')
    power = 0
else:
    s = solaredge.Solaredge(apikey)
    try: 
        r = s.get_overview(site_id)
    except:
        print("Unexpected error accessing SolarEdge portal:", sys.exc_info()[0])
        raise
    o = r["overview"]
    timestamp = int(time.mktime(time.strptime(o["lastUpdateTime"], time_pattern)))
    energy = o["lifeTimeData"]["energy"]
    power = o["currentPower"]["power"]

# DEBUG:
if args.debug:
    if r is not None:
        print(json.dumps(r, indent=4, separators=(',', ': ')))
    print("Update time: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)))
    print(graphite_pre + ".lifetime_energy " + str(energy) + ' ' + str(timestamp))
    print(graphite_pre + ".current_power " + str(power) + ' ' + str(timestamp))
else:
    graphyte.init(graphite_host, prefix=graphite_pre)
    graphyte.send('lifetime_energy', energy, timestamp=timestamp)
    graphyte.send('current_power', power, timestamp=timestamp)
