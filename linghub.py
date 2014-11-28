from urllib import quote_plus, urlopen
from urllib2 import HTTPError, URLError
import json
import sys
import urllib2
import xml.etree.ElementTree as et


def do_head(url):
    request = urllib2.Request(url)
    request.get_method = lambda: 'HEAD'

    try:
        response = urllib2.urlopen(request)
        return response.getcode() < 400
    except HTTPError:
        return False
    except URLError:
        return False

linghub_sparql = "http://linghub.lider-project.eu/sparql/?query="

dataset_query = """PREFIX void: <http://rdfs.org/ns/void#>
SELECT distinct ?dataset WHERE {
  ?dataset void:subset ?subset .
}"""

details_query = """PREFIX dc: <http://purl.org/dc/terms/>
PREFIX void: <http://rdfs.org/ns/void#>
SELECT ?links ?target ?title ?triples WHERE {
  <%s> void:triples ?triples ;
     void:subset [
       a void:LinkSet ;
       void:triples ?links ;
       void:target ?target
     ] ;
     dc:title ?title .
}"""

keyword_query = """PREFIX dcat: <http://www.w3.org/ns/dcat#>
SELECT ?keyword WHERE {
  <%s> dcat:keyword ?keyword
}"""

distribution_query = """PREFIX dcat: <http://www.w3.org/ns/dcat#>
SELECT ?dist_url WHERE {
  <%s> dcat:distribution [
    dcat:accessURL ?dist_url
  ] .
}"""

dataset_query_url = linghub_sparql + quote_plus(dataset_query)

dataset_root = et.parse(urlopen(dataset_query_url))

SR = '{http://www.w3.org/2005/sparql-results#}'

xml_results = dataset_root.find(SR + 'results').findall(SR + 'result')

datasets = {}

for result in xml_results:
    uri = result.find(SR + 'binding').find(SR + 'uri').text
    name = uri[uri.rindex('/')+1:]
    sys.stderr.write('Dataset: ' + name + '\n')
    details_query_url = linghub_sparql + quote_plus(details_query % uri)
    details_root = et.parse(urlopen(details_query_url))
    triples = -1
    subsets = {}
    title = ""
    xml_results2 = details_root.find(SR + 'results').findall(SR + 'result')
    for result2 in xml_results2:
        for binding in result2.findall(SR + 'binding'):
            var_name = binding.attrib['name']
            if var_name == 'triples':
                triples = int(binding.find(SR + 'literal').text)
            elif var_name == 'title':
                title = binding.find(SR + 'literal').text
            elif var_name == 'target':
                target = binding.find(SR + 'uri').text
                for b in (result2.findall(SR + 'binding')):
                    var_name2 = b.attrib['name']
                    if var_name2 == 'links':
                        links = int(b.find(SR + 'literal').text)
                        subsets[target] = links
    keyword_query_url = linghub_sparql + quote_plus(keyword_query % uri)
    keyword_root = et.parse(urlopen(keyword_query_url))
    keywords = []
    xml_results3 = keyword_root.find(SR + 'results').findall(SR + 'result')
    for result3 in xml_results3:
        keywords.append(result3.find(SR + 'binding').find(SR + 'literal').text)
    dist_query_url = linghub_sparql + quote_plus(distribution_query % uri)
    dist_root = et.parse(urlopen(dist_query_url))
    dists = []
    xml_results4 = dist_root.find(SR + 'results').findall(SR + 'result')
    for result4 in xml_results4:
        dists.append(result4.find(SR + 'binding').find(SR + 'uri').text)
    aliveurls = 0
    deadurls = 0
    for dist in dists:
        sys.stderr.write("checking " + dist)
        if do_head(dist):
            aliveurls += 1
            sys.stderr.write(" [OK]\n")
        else:
            deadurls += 1
            sys.stderr.write(" [FAIL]\n")

    if aliveurls > 0:
        datasets[name] = {
            'triples': triples,
            'links': subsets,
            'name': title,
            'url': uri,
            'tags': keywords,
            'aliveurls': aliveurls,
            'deadurls': deadurls
        }

print(json.dumps(datasets, indent=4))
