#!/usr/bin/python

import sys

fsameas = open(sys.argv[1])
fdbrels = open(sys.argv[2])
ffbrels = open(sys.argv[3])

sameAs = {}

for line in fsameas.readlines():
    line = line.strip()
    content = line.split(' sameAs ')
    sameAs[content[1]] = content[0]
fsameas.close()

dbrels = {}

for line in fdbrels.readlines():
    line = line.strip()
    content = line.split(' ')
    dbo,rel,dbp = content[0],content[1],content[2]
    if dbo not in dbrels:
        dbrels[dbo] = []
        dbrels[dbo].append((rel,dbp))
fdbrels.close()

fbrels = {}                          

for line in ffbrels.readlines():     
    line = line.strip()              
    content = line.split(' ')        
    fbo,rel,fbp = content[0],content[1],content[2]                         
    if fbo not in fbrels:
        fbrels[fbo] = []
        fbrels[fbo].append((rel,fbp))
ffbrels.close()


def dbsameas(var):
    return sameAs[var]

def dbhassameas(var):
    if var in sameAs:
        return True

def dbrelated(o,p):
    if o in sameAs:
        arr = sameAs[o]
        for t in arr:
            if p == t[1]:
                return True
    if p in sameAs:
        arr = sameAs[p]
        for t in arr:
            if o == t[1]:
                return True
    return False   
 

for fbo,rels in fbrels.items():
    for r,fbp in rels:
        if dbhassameas(fbo) and dbhassameas(fbp):
            if not dbrelated(dbsameas(fbo),dbsameas(fbp)):
                print "Potential relation: %s->%s->%s"%(dbsameas(fbo),r,dbsameas(fbp))



















