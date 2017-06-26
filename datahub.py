import urllib2
import json
import re
import sys

from urllib2 import HTTPError, URLError

# todos:
# - check on runtime whether the URLs given are alive
# ok ... but now it's REALLY slow
# - check on runtime whether format is RDF or OWL
# for many dataset, the metadata is incomplete, e.g., dbpedia-ko, hence later

# meta data categories:
# via tags:
# "corpus" => llod:corpus
# "lexicon", "wordnet" => llod:corpus
# (none of these) => llod:language_description

print("DataHub LLOD cloud generator")
sys.stdout.flush()

baseURL = "http://datahub.io/api/3/action/"
blacklist = [
    'ss', 																					# spam
    'cgsddforja', 																			# spam
    'sqxfetge', 																			# spam
    'fafqwfaf', 																			# spam
    'sqxfetgea', 																			# spam
    """cosmetic-surgeon-wearing-nursing-scrubs-nursing-uniforms-
expert-scrubs-for-safety""" 	# spam
]

license_uris = {
    "cc-by": "http://www.opendefinition.org/licenses/cc-by",
    "cc-by-sa": "http://www.opendefinition.org/licenses/cc-by-sa",
    "cc-nc": "http://www.opendefinition.org/licenses/cc-nc",
    "cc-zero": "http://www.opendefinition.org/licenses/cc-zero",
    "gfdl": "http://www.opendefinition.org/licenses/gfdl",
    "odc-by": "http://www.opendefinition.org/licenses/odc-by",
    "odc-odbl": "http://www.opendefinition.org/licenses/odc-odbl",
    "odc-pddl": "http://www.opendefinition.org/licenses/odc-pddl",
    "other-at": "attribution",
    "other-closed": "closed",
    "other-nc": "nc",
    "other-open": "open",
    "other-pd": "public-domain",
    "uk-ogl": "http://reference.data.gov.uk/id/open-government-licence"
}




def ckanListDatasetsInGroup(group):
    url = baseURL + "package_search?rows=200&fq=organization:" + group
    return json.loads(urllib2.urlopen(url).read())


def ckanListDatasetsForTag(tag):
    #url = baseURL + "tag_show?id=" + tag
    url = baseURL + "package_search?rows=200&fq=tags:" + tag
    return json.loads(urllib2.urlopen(url).read())


def ckanDataset(dataset):
    url = baseURL + "package_show?id=" + dataset
    return json.loads(urllib2.urlopen(url).read())

nodes = {}

# NEW: check not only group data sets, but everything with a corresponding tag

datasetJSON = ckanListDatasetsInGroup("owlg")
datasets = [ds["name"] for ds in datasetJSON["result"]["results"]]
print "group 'owlg': "+str(len(datasets))+" datasets"
sys.stdout.flush()
for group in ["mlode2012", "sfb673"]:
    newDatasetJSON = ckanListDatasetsInGroup(group)
    newDatasets = [ds["name"] for ds in newDatasetJSON["result"]["results"]]
    datasets = datasets + newDatasets
    datasets = list(set(datasets))
    print "+ group '"+group+"': "+str(len(datasets))+" datasets"
    sys.stdout.flush()
for tag in ["llod", "linguistics%20lod", "lexicon", "corpus", "thesaurus",
            "isocat", "linguistic", "linguistics", "typology", "lrec-2014",
            "lexical-resources"]:
    newDatasetJSON = ckanListDatasetsForTag(tag)
    newDatasets = [ds["name"] for ds in newDatasetJSON["result"]["results"]]
    datasets = datasets + newDatasets
    datasets = list(set(datasets))
    print "+ tag '"+tag+"': "+str(len(datasets))+" datasets"
    sys.stdout.flush()

datasets = set(datasets) - set(blacklist)
print "- blacklist: "+str(len(datasets))+" datasets"
sys.stdout.flush()

for dataset in datasets:
    nodes[dataset] = {}
    nodes[dataset]["edgecount"] = 0


for dataset in datasets:
    print("Dataset:" + dataset)
    sys.stdout.flush()
    dsJSON = ckanDataset(dataset)
    nodes[dataset]["url"] = baseURL + "package_show?id=" + dataset
    nodes[dataset]["name"] = dsJSON["result"]["title"]
    nodes[dataset]["links"] = {}
    nodes[dataset]["tags"] = []
    nodes[dataset]["aliveurls"] = 0
    nodes[dataset]["deadurls"] = 0
    nodes[dataset]["formats"] = 0
    nodes[dataset]["rdf_owl"] = 0
    nodes[dataset]["email"] = dsJSON["result"]["maintainer_email"]
    if dsJSON["result"]["license_id"] in license_uris:
        nodes[dataset]["license"] = (
            license_uris[dsJSON["result"]["license_id"]])

    for tag in dsJSON["result"]["tags"]:
        nodes[dataset]["tags"].extend([tag["name"]])

    # check whether URLs given are alive
    try:
        try:
            urllib2.urlopen(urllib2.Request(dsJSON["result"]["url"]),
                            timeout=15)
        except HTTPError as e:
            print("HTTPError " + str(e.code) + " while trying to access " +
                  dsJSON["result"]["url"])
            nodes[dataset]["deadurls"] += 1
        except ValueError:
            try:
                urllib2.urlopen(urllib2.Request("http://" +
                                                dsJSON["result"]["url"]),
                                timeout=15)
            except HTTPError as e1:
                print("HTTPError " + str(e1.code) + " while trying to access "
                      + dsJSON["result"]["url"])
                nodes[dataset]["deadurls"] += 1
            except URLError as e1:
                print("URLError " + e1.reason + " while trying to access "
                      + dsJSON["result"]["url"])
                nodes[dataset]["deadurls"] += 1
            else:
                nodes[dataset]["aliveurls"] += 1
        except URLError as e:
            try:
                print("URLError " + e.reason + " while trying to access "
                      + dsJSON["result"]["url"])
            except TypeError:
                print "URLError"
            nodes[dataset]["deadurls"] += 1
        except AttributeError as e:
            print "AttributeError"
            nodes[dataset]["deadurls"] += 1
        else:
            nodes[dataset]["aliveurls"] += 1
    except:
        print "Error"

    for res in dsJSON["result"]["resources"]:
        try:
            try:
                urllib2.urlopen(urllib2.Request(res["url"]), timeout=15)
            except HTTPError as e:
                print("HTTPError " + str(e.code) + " while trying to access "
                      + res["url"])
                nodes[dataset]["deadurls"] += 1
            except ValueError:
                try:
                    urllib2.urlopen(urllib2.Request("http://"+res["url"]),
                                    timeout=15)
                except HTTPError as e1:
                    print("HTTPError " + str(e1.code) +
                          " while trying to access "+res["url"])
                    nodes[dataset]["deadurls"] += 1
                except URLError as e1:
                    print("HTTPError " + e1.reason + " while trying to access "
                          + res["url"])
                    nodes[dataset]["deadurls"] += 1
                else:
                    nodes[dataset]["aliveurls"] += 1
            except URLError as e:
                try:
                    print("URLError " + e.reason + " while trying to access "
                          + res["url"])
                except TypeError:
                    print "URLError"
                nodes[dataset]["deadurls"] += 1
            else:
                nodes[dataset]["aliveurls"] += 1
        except:
            print "Error"
    print("alive: " + str(nodes[dataset]["aliveurls"]) + "/" +
          str(nodes[dataset]["aliveurls"] + nodes[dataset]["deadurls"]))
    sys.stdout.flush()

    # count links
    for kv in dsJSON["result"]["extras"]:
        if(re.match("links:.*", kv["key"])):
            target = kv["key"][6:]
            try:
                s = float(kv["value"][0:(len(kv["value"]))])
            except ValueError:
                s = 50  # default: assume 50 links
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
    with open("llod-cloud.json", "w") as outfile:
        json.dump(nodes, outfile, indent=4)

with open("excluded-resources.csv", "w") as outfile:
    outfile.write("ID,Title,Issue,Email\n")
    # since LDL-2014, we exclude unlinked data sets
    for v in nodes.keys():
        if(nodes[v]["edgecount"] == 0):
            print("remove %s due to no links (email: %s)" %
                  (nodes[v]["name"], nodes[v]["email"]))
            outfile.write("%s,\"%s\",\"No links\",%s\n" %
                          (v, nodes[v]["name"], nodes[v]["email"]))
            del nodes[v]

    sys.stdout.flush()

    # we exclude everything that's totally down
    for v in nodes.keys():
        if(nodes[v]["aliveurls"] == 0):
            print("remove %s as no URLs resolve (email: %s)" %
                  (nodes[v]["name"], nodes[v]["email"]))
            outfile.write("%s,\"%s\",\"Does not resolve\",%s\n" %
                          (v, nodes[v]["name"], nodes[v]["email"]))
            del nodes[v]

sys.stdout.flush()

with open("llod-cloud.json", "w") as outfile:
    json.dump(nodes, outfile, indent=4)
