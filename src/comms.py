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

if len(sys.argv) > 1:
    port = sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

while True:
    topic = 001
    messagedata = random.randrange(1,215) - 80
    print "%d %d" % (topic, messagedata)
    socket.send("%d %d" % (topic,messagedata))
    time.sleep(5)


