#!/usr/bin/python


import sys,os,json
import requests
from multiprocessing import Pool

f = open(sys.argv[1])
lines = []
for line in f.readlines():
    line = line.strip()
    lines.append(line)
 

def find(line):
    try:
        if 'sameAs' not in line:
            return []
        dbpl = line.split(' ')[0]
        dbpl = dbpl.split('dbpedia:')[1]
        q = """SELECT ?o
           WHERE 
           {
           <http://dbpedia.org/resource/%s> <http://www.w3.org/2002/07/owl#sameAs>  ?o.
           filter regex(?o, "freebase")
           }"""%dbpl
        url = "http://dbpedia.org/sparql"
        p = {'query': q}
        h = {'Accept': 'application/json'}
        r = requests.get(url, params=p, headers=h)
        d =json.loads(r.text)
        for row in d['results']['bindings']:
            print "%s sameAs %s"%(dbpl,row['o']['value'])
            sys.stdout.flush()
    except Exception,e:
        print e
    return None



if __name__ == '__main__':
    p = Pool(1)
    p.map(find, lines)


