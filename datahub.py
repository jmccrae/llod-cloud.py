import urllib2
import json
import re
import math

baseURL = "http://datahub.io/api/3/action/"
blacklist = ['apertium', # not rdf
'wiktionary-en', # not rdf
'wordnet', # not rdf
'sanskrit-english-lexicon', # down
'saldo', # not rdf
'xwn', # not rdf
'talkbank', # not rdf
'french-timebank', # not rdf
'jmdict', # not rdf
'multext-east', # not rdf
'cosmetic-surgeon-wearing-nursing-scrubs-nursing-uniforms-expert-scrubs-for-safety', # spam?
'pali-english-lexicon', # down
'printed-book-auction-catalogues', # down
'wikiword_thesaurus', # not rdf
'eu-dgt-tm', # not rdf
'masc', # rdf export... not linked data
'multilingualeulaw', # not rdf
'wiktionary', # not rdf
'omegawiki', # not rdf
'framenet', # not rdf
'o-anc', # not rdf
'conceptnet', # not rdf
'phoible', # not rdf
'dbpedia-spotlight', # tool not data!
'opus', # not rdf
'ss', # spam
'cgsddforja', # spam
'sqxfetge', # spam
'fafqwfaf', # spam
'sqxfetgea', # spam
'analisi-del-blog-http-www-beppegrillo-it' # spam
]

def ckanListDatasetsInGroup(group):
  url = baseURL + "group_show?id=" + group
  return json.loads(urllib2.urlopen(url).read())

def ckanDataset(dataset):
  url = baseURL + "package_show?id=" + dataset
  return json.loads(urllib2.urlopen(url).read())

nodes = {}

datasetJSON = ckanListDatasetsInGroup("linguistics")
datasets = [ds["name"] for ds in datasetJSON["result"]["packages"]]
datasets = set(datasets) - set(blacklist)
for dataset in datasets:
  nodes[dataset] = {}
  nodes[dataset]["edgecount"] = 0

for dataset in datasets:
  print("Dataset:" + dataset)
  dsJSON = ckanDataset(dataset)
  nodes[dataset]["url"] = baseURL + "package_show?id=" + dataset
  nodes[dataset]["name"] = dsJSON["result"]["title"]
  nodes[dataset]["links"] = {}
  for kv in dsJSON["result"]["extras"]:
    if(re.match("links:.*",kv["key"])):
      target = kv["key"][6:]
      s = float(kv["value"][0:(len(kv["value"]))])
      print(dataset + " => " + target + ": weight " + kv["value"])
      if target in nodes.keys():
        nodes[dataset]["links"][target] = s
        nodes[dataset]["edgecount"] += 1
        nodes[target]["edgecount"] += 1
      else:
        print("External edge:" + target)
    if(kv["key"] == "triples"):
      nodes[dataset]["triples"] = kv["value"][1:(len(kv["value"])-1)]

#for v in nodes.keys():
#  if(nodes[v]["edgecount"] == 0):
#    del nodes[v]

with open("llod-cloud.json","w") as outfile:
  json.dump(nodes,outfile,indent=4)
