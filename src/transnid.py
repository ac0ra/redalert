#!/bin/env python
###
###
###
Author = 'Adam Grigolato'
Version = '0'
###
###
###
import json

class nid(object):
    def __init__(self, trans, var2):
        self.trans = trans
        self.var2 = var2
    def __repr__(self):
        #return '<(%s)(%s)>' % self.trans,self.var2
        return "<({0})({1})>".format(self.trans, self.var2)


class cryptonid(object):
    def __init__(self, key):
        self.key = key
    def __repr__(self):
        return '<(%s)>' % self.key

class encoder(json.JSONEncoder):

    def default(self, obj):
        print 'default(', repr(obj), ')'
        d = { '__class__':obj.__class__.__name__,'__module__':obj.__module__, }
        d.update(obj.__dict__)
        return d

class decoder(json.JSONDecoder):
    
    def __init__(self):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)

    def dict_to_object(self, d):
        if '__class__' in d:
            class_name = d.pop('__class__')
            module_name = d.pop('__module__')
            module = __import__(module_name)
            print 'MODULE:', module
            class_ = getattr(module, class_name)
            print 'CLASS:', class_
            args = dict( (key.encode('ascii'), value) for key, value in d.items())
            print 'INSTANCE ARGS:', args
            inst = class_(**args)
        else:
            inst = d
        return inst
