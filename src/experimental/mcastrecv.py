#!/bin/env python
###
###
###
Author = 'Adam Grigolato'
Version = '0'
###
###
###
from base64 import b64encode
import socket
import struct
import os
import json
from netaddr import *

MCAST_GRP = '224.1.1.192'
MCAST_PORT = 8472

network = {}
hosts = {}

def getnet(ip):
    net = IPNetwork(ip)
    return str(net.cidr) 

def networkadd(id, cidr):
    revnetwork = {}
    global network
    revnetwork = {value:key for key, value in network.iteritems()}
    if cidr in revnetwork:
        return revnetwork.get(cidr)
    else:
        for n in range(35535):
            if n not in network:
                network[n] = cidr
                return n

#def networkdel(id, ip):

#def networksort():

#def hostadd(nid, id, ip, port):

#def hostfind(nid, id, ip, port):

#def hostdel(nid, id):

#def hostsort():

def mcastrecv():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except AttributeError:
        pass
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

    sock.bind((MCAST_GRP,MCAST_PORT))
    host = socket.gethostbyname(socket.gethostname())
    sock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
    sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(MCAST_GRP) + socket.inet_aton(host))

    while 1:
        try:
            data, addr = sock.recvfrom(1024)
        except socket.error, e:
            print 'Exception'
        #print 'Data = %s' % data
        ddata = json.loads(data)
        for key, value in ddata.items():
            print key, value
        #recv_json = json.dumps(ddata, sort_keys=True, indent=2)
        #print 'JSON:', recv_json



if __name__ == '__main__':
        mcastrecv()
