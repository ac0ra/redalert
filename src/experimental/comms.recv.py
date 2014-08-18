#!/bin/env python
###
###
###
Author = 'Adam Grigolato'
Version = '0'
###
###
###

### IMPORTS ###

import zmq
import time
import random
import sys


port = 8473
host = "localhost"

if len(sys.argv) > 1:
    port = sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.SUB)

print "Collecting Updates from Master(%s:%s)" % (host,port)
connection = socket.connect ("tcp://%s:%s" % (host,port))
