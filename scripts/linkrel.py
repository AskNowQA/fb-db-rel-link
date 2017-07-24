#!/usr/bin/python

import sys

fsameas = open(sys.argv[1])
fdbrels = open(sys.argv[2])
ffbrels = open(sys.argv[3])

sameAs = {}

for line in fsameas.readlines():
    line = line.strip()
    content = line.split(' sameAs ')
    sameAs[content[0]] = content[1]
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


def fbsameas(var):
    return sameAs[var]

def fbhassameas(var):
    if var in sameAs:
        return True
    else:
        return False

def fbrelexists(o,p):
    if o in fbrels:
        arr = fbrels[o]
        for t in arr:
            if p == t[1]:
                return True
    if p in fbrels:
        arr = fbrels[p]              
        for t in arr:                
            if o == t[1]:            
                return True
    return False

def dbrelations(o,p):
    relations = []
    if o in dbrels:
        for t in dbrels[o]:
            if p == t[1]:
                relations.append(t[0])
    if p in dbrels:
        for t in dbrels[p]:
            if o == t[1]:
                relations.append(t[0])
    return relations

def fbrelations(o,p):
    relations = []
    if o in fbrels:
        for t in fbrels[o]:
            if p == t[1]:
                relations.append(t[0])
    if p in fbrels:
        for t in fbrels[p]:
            if o == t[1]:
                relations.append(t[0])
    return relations


for dbo,rels in dbrels.items():
    for r,dbp in rels:
        if dbo == dbp:
            continue
        if fbhassameas(dbo) and fbhassameas(dbp):
#            print dbo,' ',r,' ',dbp,' ',fbsameas(dbo),' ',fbsameas(dbp)
            if fbrelexists(fbsameas(dbo), fbsameas(dbp)):
                print "Relationships found: %s %s <----> %s %s"%(dbo,dbp,fbsameas(dbo),fbsameas(dbp))
                print "dbrelations:"
                print dbrelations(dbo,dbp)
                print "fbrelations:"
                print fbrelations(fbsameas(dbo),fbsameas(dbp))

