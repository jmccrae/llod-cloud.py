import urllib
import urllib2
import json
import re
import math

from urllib2 import HTTPError, URLError 

# todos: 
# - check on runtime whether the URLs given are alive	# ok ... but now it's REALLY slow
# - check on runtime whether format is RDF or OWL		# for many dataset, the metadata is incomplete, e.g., dbpedia-ko, hence later

# meta data categories:
# via tags:
# "corpus" => llod:corpus
# "lexicon", "wordnet" => llod:corpus
# (none of these) => llod:language_description

baseURL = "http://datahub.io/api/3/action/"
blacklist = [
# CC: we filter for triples attribute, hence eliminating all non-rdf resources
	# 'apertium', 																			# not rdf
	# 'wiktionary-en', 																		# not rdf
	# 'wordnet', 																			# not rdf
	# 'saldo', 																				# not rdf
	# 'xwn', 																				# not rdf
	# 'talkbank', 																			# not rdf
	# 'french-timebank', 																	# not rdf
	# 'jmdict', 																			# not rdf
	# 'multext-east', 																		# not rdf
	# 'wikiword_thesaurus', 																# not rdf
	# 'eu-dgt-tm', 																			# not rdf
	# 'multilingualeulaw', 																	# not rdf
	# 'wiktionary', 																		# not rdf
	# 'omegawiki', 																			# not rdf
	# 'framenet', 																			# not rdf
	# 'o-anc', 																				# not rdf
	# 'conceptnet', 																		# not rdf
	# 'opus', 																				# not rdf
	# 'analisi-del-blog-http-www-beppegrillo-it', 											# not rdf
'dbpedia-spotlight', 																	# tool not data
'ss', 																					# spam
'cgsddforja', 																			# spam
'sqxfetge', 																			# spam
'fafqwfaf', 																			# spam
'sqxfetgea', 																			# spam
'printed-book-auction-catalogues', 														# spam ?
'cosmetic-surgeon-wearing-nursing-scrubs-nursing-uniforms-expert-scrubs-for-safety' 	# spam
]

def ckanListDatasetsInGroup(group):
  url = baseURL + "group_list?id=" + group
  return json.loads(urllib2.urlopen(url).read())

def ckanListDatasetsForTag(tag):
  url = baseURL + "tag_show?id=" + tag
  return json.loads(urllib2.urlopen(url).read())
  
def ckanDataset(dataset):
  url = baseURL + "package_show?id=" + dataset
  return json.loads(urllib2.urlopen(url).read())

nodes = {}

# NEW: check not only group data sets, but everything with a corresponding tag

#datasetJSON = ckanListDatasetsInGroup("owlg")
#datasets = [ds["name"] for ds in datasetJSON["result"]["packages"]]	
#print "group 'owlg': "+str(len(datasets))+" datasets"
datasets = []
#for group in ["mlode2012", "sfb673"]:
#	newDatasetJSON = ckanListDatasetsInGroup(group)
#	newDatasets = [ds["name"] for ds in newDatasetJSON["result"]["packages"]]
#	datasets = datasets + newDatasets
#	datasets = list(set(datasets))
#	print "+ group '"+group+"': "+str(len(datasets))+" datasets"
for tag in ["llod", "linguistics%20lod", "lexicon", "corpus", "thesaurus", "isocat", "linguistic", "linguistics", "typology", "lrec-2014"]:
	 newDatasetJSON = ckanListDatasetsForTag (tag)
	 newDatasets = [ds["name"] for ds in newDatasetJSON["result"]["packages"]]
	 datasets = datasets + newDatasets
	 datasets = list(set(datasets))
	 print "+ tag '"+tag+"': "+str(len(datasets))+" datasets"
		
datasets = set(datasets) - set(blacklist)
print "- blacklist: "+str(len(datasets))+" datasets"

for dataset in datasets:
  nodes[dataset] = {}
  nodes[dataset]["edgecount"] = 0

for dataset in datasets:
  print("Dataset:" + dataset)
  dsJSON = ckanDataset(dataset)
  nodes[dataset]["url"] = baseURL + "package_show?id=" + dataset
  nodes[dataset]["name"] = dsJSON["result"]["title"]
  nodes[dataset]["links"] = {}
  nodes[dataset]["tags"] = []
  nodes[dataset]["aliveurls"] = 0
  nodes[dataset]["deadurls"] = 0
  nodes[dataset]["formats"] = 0
  nodes[dataset]["rdf_owl"] = 0
   
  for tag in dsJSON["result"]["tags"]:
    nodes[dataset]["tags"].extend([tag["name"]])
   
  # check whether URLs given are alive
  try:
    try: urllib2.urlopen(urllib2.Request(dsJSON["result"]["url"]))
    except HTTPError as e:
      print "HTTPError "+str(e.code)+" while trying to access "+dsJSON["result"]["url"]
      nodes[dataset]["deadurls"] += 1
    except ValueError:
      try: urllib2.urlopen(urllib2.Request("http://"+dsJSON["result"]["url"]))
      except HTTPError as e1:
        print "HTTPError "+str(e1.code)+" while trying to access "+dsJSON["result"]["url"]
        nodes[dataset]["deadurls"] += 1
      except URLError as e1:
        print "URLError "+e1.reason+" while trying to access "+dsJSON["result"]["url"]
        nodes[dataset]["deadurls"] += 1
      else: nodes[dataset]["aliveurls"] += 1
    except URLError as e:
      try: print "URLError "+e.reason+" while trying to access "+dsJSON["result"]["url"]
      except TypeError:
        print "URLError"
      nodes[dataset]["deadurls"] += 1
    except AttributeError as e:
      print "AttributeError"
      nodes[dataset]["deadurls"] += 1
    else: nodes[dataset]["aliveurls"] += 1
  except:
    print "Error"

  for res in dsJSON["result"]["resources"]:
    try:
      try: urllib2.urlopen(urllib2.Request(res["url"]))
      except HTTPError as e:
        print "HTTPError "+str(e.code)+" while trying to access "+res["url"]
        nodes[dataset]["deadurls"] += 1
      except ValueError:
        try: urllib2.urlopen(urllib2.Request("http://"+res["url"]))
        except HTTPError as e1:
          print "HTTPError "+str(e1.code)+" while trying to access "+res["url"]
          nodes[dataset]["deadurls"] += 1
        except URLError as e1:
          print "HTTPError "+e1.reason+" while trying to access "+res["url"]
          nodes[dataset]["deadurls"] += 1
        else: nodes[dataset]["aliveurls"] += 1
      except URLError as e:
        try: print "URLError "+e.reason+" while trying to access "+res["url"]
        except TypeError:
           print "URLError"	  
        nodes[dataset]["deadurls"] += 1
      else: nodes[dataset]["aliveurls"] += 1
    except:
      print "Error"
  print("alive: " +str(nodes[dataset]["aliveurls"])+"/"+str(nodes[dataset]["aliveurls"]+nodes[dataset]["deadurls"]))
	
	 
  # count links
  for kv in dsJSON["result"]["extras"]:
    if(re.match("links:.*",kv["key"])):
      target = kv["key"][6:]
      try: s = float(kv["value"][0:(len(kv["value"]))])
      except ValueError:
        s=50; # default: assume 50 links
      print(dataset + " => " + target + ": weight " + kv["value"])
      if target in nodes.keys():
        nodes[dataset]["links"][target] = s
        nodes[dataset]["edgecount"] += 1
        nodes[target]["edgecount"] += 1
      else:
        print("External edge:" + target)
    if(kv["key"] == "triples"):
      # nodes[dataset]["triples"] = kv["value"][1:(len(kv["value"])-1)]
	  nodes[dataset]["triples"] = kv["value"]

  # for debugging only (final dump at the end)
  with open("llod-cloud.json","w") as outfile:
    json.dump(nodes,outfile,indent=4)
	  
# since LDL-2014, we exclude unlinked data sets
for v in nodes.keys():
  if(nodes[v]["edgecount"] == 0):
    del nodes[v]

# we exclude everything that's totally down
for v in nodes.keys():
  if(nodes[v]["aliveurls"] == 0):
    del nodes[v]

with open("llod-cloud.json","w") as outfile:
  json.dump(nodes,outfile,indent=4)
