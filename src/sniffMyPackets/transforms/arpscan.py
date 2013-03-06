#!/usr/bin/env python

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
#from canari.maltego.utils import debug, progress
from canari.maltego.message import Field, MatchingRule
from canari.framework import configure #, superuser
from common.ipaddrchanges import *
from common.entities import WirelessCard, Gateway
from canari.maltego.entities import IPv4Address

__author__ = 'catalyst256'
__copyright__ = 'Copyright 2013, Sniffmypackets Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'catalyst256'
__email__ = 'catalyst256@gmail.com'
__status__ = 'Development'

__all__ = [
    'dotransform'
]


#@superuser
@configure(
    label='ARP Scan [A]',
    description='Performs ARP scan when connected to wireless network',
    uuids=[ 'sniffMyPackets.v2.ARPScan' ],
    inputs=[ ( 'sniffMyPackets', Gateway ) ],
    debug=True
)
def dotransform(request, response):
	
	if 'sniffMyPackets.int2gw' in request.fields:
	  interface = request.fields['sniffMyPackets.int2gw']
	if 'sniffMyPackets.gwmac' in request.fields:
	  gateway = request.fields['sniffMyPackets.gwmac']

	conf.iface=interface
	subnet = ''
	network = ''
	cidr = ''
	arpscan = []
	
	for x in conf.route.routes:
	  if x[3] == interface and x[2] == '0.0.0.0':
		subnet = x[1]
		network = x[0]
	
	subnet = subnetAddress(subnet)
	cidr = cidr2subnet(subnet)
	network = networkAddress(network)
		
	ans,uans = arping(str(network)+'/'+str(cidr), verbose=0)
	for send,rcv in ans:
	  e = IPv4Address(rcv.sprintf("%ARP.psrc%"))
	  e.internal = True
	  e += Field('ethernet.hwaddr', rcv.sprintf("%Ether.src%"), displayname='Hardware Address', matching_rule=MatchingRule.Strict)
	  e += Field('gateway.hwaddr', gateway, displayname='Gateway Address', matching_rule=MatchingRule.Strict)
	  response += e
	return response

