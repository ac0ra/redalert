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
import ast



MCAST_GRP = '224.1.1.192'
MCAST_PORT = 8472


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
        print 'Data = %s' % data
        ddata = json.loads(data)
        recv_json = json.dumps(ddata, sort_keys=True, indent=2)
        print 'JSON:', recv_json



if __name__ == '__main__':
        mcastrecv()
