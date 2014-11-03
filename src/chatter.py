#!/bin/env python
###
###
###
Author = 'Adam Grigolato'
Version = '0'
###
###
###

import socket
import struct
import binascii


MCAST_GRP = '224.1.1.192'
MCAST_PORT = 8472

def mcastsend(MCAST_MSG):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    sock.sendto(MCAST_MSG, (MCAST_GRP, MCAST_PORT))


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
        hexdata = binascii.hexlify(data)
        print 'HexData = %s' % hexdata
        print 'Data = %s' % data







if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Send or recieve multicast test')
    parser.add_argument('--receive', help='Receive Multicast tester',action="store_true")
    parser.add_argument('--send', help='Send Multicast Tester')
    args = parser.parse_args()
    if args.receive:
        mcastrecv()
    elif args.send:
        mcastsend(args.send)

