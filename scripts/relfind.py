#!/usr/bin/python

import sys,os,json
import requests

f = open(sys.argv[1])

lines = []
for line in f.readlines():
    line = line.strip()
    lines.append(line)
    

fbls = {}
for line in lines:
    fbl = line.split(' ')[0]
    fbls[fbl] = False
del lines

for fbl,val in fbls.items():
    if val:
        continue
    q = """SELECT ?p ?o
           WHERE                     
           {                         
           <http://dbpedia.org/resource/%s> ?p  ?o                                  
           }"""%fbl                
    url = "http://dbpedia.org/sparql"                                  
    p = {'query': q}             
    h = {'Accept': 'application/json'}                                 
    r = requests.get(url, params=p, headers=h)                         
    print r
    d =json.loads(r.text)
    for row in d['results']['bindings']:
        if row['o']['value'] in fbls:
            print "%s %s:%s %s:%s"%(fbl, row['p']['type'], row['p']['value'], row['o']['type'], row['o']['value'])
            sys.stdout.flush()
            fbls[fbl] = True
            fbls[row['o']['value']] = True
    q = """SELECT ?s ?p
           WHERE                                                           
           {                                                               
           ?s ?p  <http://dbpedia.org/resource/%s>                                  
           }"""%fbl                  
    url = "http://dbpedia.org/sparql"                                      
    p = {'query': q}                 
    h = {'Accept': 'application/json'}                                     
    r = requests.get(url, params=p, headers=h)                             
    print r
    d =json.loads(r.text)
    for row in d['results']['bindings']:                                   
        if row['s']['value'] in fbls:
            print "%s:%s %s:%s %s"%(row['s']['type'], row['s']['value'], row['p']['type'], row['p']['value'], fbl)
            sys.stdout.flush()
            fbls[fbl] = True
            fbls[row['s']['value']] = True
