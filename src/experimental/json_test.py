#!/bin/env python
###
###
###
Author = 'Adam Grigolato'
Version = '0'
###
###
###
import sys
sys.path.append('../')

import json
import transnid

obj = transnid.nid('testing', 'variable2')

print obj
encoded = transnid.encoder().encode(obj)
print encoded
decoded = transnid.decoder().decode(encoded)
print decoded
