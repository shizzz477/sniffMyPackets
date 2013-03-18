#!/usr/bin/env python


import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
#from canari.maltego.utils import debug, progress
from common.entities import pcapFile
from canari.maltego.entities import IPv4Address
from canari.maltego.message import Field
from canari.framework import configure #, superuser

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
    label='Find TCP talkers [pcap]',
    description='Search a pcap file and return all talkers',
    uuids=[ 'sniffMyPackets.v2.pcap2talkers' ],
    inputs=[ ( 'sniffMyPackets', pcapFile ) ],
    debug=True
)
def dotransform(request, response):
    
    talkers = []
    pkts = rdpcap(request.value)
    for x in pkts:
      if x.haslayer(TCP) and x.getlayer(TCP).flags == 0x002:
	src = x.getlayer(IP).src
	if src not in talkers:
	  talkers.append(src)
    for s in talkers:
      e = IPv4Address(s)
      e += Field('pcapsrc', request.value, displayname='Original pcap File', matchingrule='loose')
      response += e
    return response
