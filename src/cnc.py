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
import os
import os.path
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256
import json
from chatter import mcastrecv,mcastsend



## TO DO ##
# Cluster tasks,
# Task:
# INFORM { Inform the cluster of changes to localy authoritive configuration }
# ELECT { Election called for a sub cluster responsibility }
# CONNECT { Connection request to the cluster }
# DISCONNECT { Disconnect from the cluster }
# 


def generate_new_keypair(keysize):
    rgen = Random.new().read
    return RSA.generate(keysize, rgen)

def get_conf_hash(config):
    return SHA256.new(config).hexdigest()

def check_conf_hash(config,newconfhash):
    return SHA256.new(config).hexdigest() == newconfhash

def pubkey_manage(action, location, key='null'):
    if action == 'save':
        f = open(location,'w')
        f.write(key.exportKey('OpenSSH'))
        f.close()
    elif action == 'load':
        f = open(location,'r')
        key = RSA.importKey(f.read())
        return key

config = "{'netid': '2810', 'netconf': { 'ipaddress': '172.24.168.26', 'port': '8473', 'mask': '20' } } "

clientID = '1337'


if os.path.isfile("./localkey.priv") == False:
    hostkey = generate_new_keypair(8192)
    pubkey_manage('save', './localkey.priv', hostkey)
else:
    hostkey = pubkey_manage('load', './localkey.priv')
   
#public_hostkey = base64.b64encode(base64.b16decode(hostkey.upper()))
public_hostkey = '%s' % (hostkey.publickey())
bpubkey = b64encode(public_hostkey)


confhash = get_conf_hash(config)

command = config

testconnectlet = [ { 'clientID': 'random','pubkey': 'pubkey', 'confhash': 'confhash', 'CONNECT': { 'netid': 'netid', 'netconf': { 'ipaddress': 'ipaddr', 'port': 'portnumber', 'mask': 'mask' } } } ]
commandlet = { 'clientID': 'clientid', 'pubkey': 'pubkey', 'confhash': 'pubkey', 'command':'command', 'parameters':'null'}
cryptolet = { 'destpubkey': 'dpk', 'ciphertext': 'ctext'}

def modjson(adict, k, v):
    for key in adict.keys():
        if key == k:
            adict[key] = v
        elif type(adict[key]) is dict:
            modjson(adict[key], k, v)

def assemble_command(crypto,command, clientID, pubkey, confhash, config):
    if crypto == False:
        if command == 'connect':
            modjson(commandlet, 'clientID', clientID)
            modjson(commandlet, 'pubkey', pubkey)
            modjson(commandlet, 'confhash', confhash)
            modjson(commandlet, 'command', command)
            modjson(commandlet, 'parameters', config)
    elif crypto == True:
        if command == 'connect':
            assemble_command(False, 'connect', clientID, bpubkey, confhash, config)
            modjson(commandlet,


assemble_command(False, 'connect', clientID, bpubkey, confhash, config)

data_string = json.dumps(commandlet, sort_keys=True, indent=2)
print 'ENCODED:', data_string


crypto_string = json.dumps(cryptolet, sort_keys=True, indent=2)
print 'ENCRYPTED:', crypto_string

print 'Sending Connect String Via Multicast'

mcastsend(str(commandlet))
