#-*- coding: utf-8 -*-

import re
import json
import math
import datetime
import sys

# we write directly GraphML as manually produced by yEd, but perform no positioning
# for automated positioning, open the file, e.g., in yEd, and generate a proper layout, (e.g., yEd's "organic")


edgeBaseSize=3
vertexBaseSize=10
canvas=4000

data = json.load(open("llod-cloud.json"))

graphml=open("llod-cloud.graphml","w")
# write header
graphml.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n\
<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:y="http://www.yworks.com/xml/graphml" xmlns:yed="http://www.yworks.com/xml/yed/3" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd">\n\
  <key for="graphml" id="d0" yfiles.type="resources"/>\n\
  <key for="port" id="d1" yfiles.type="portgraphics"/>\n\
  <key for="port" id="d2" yfiles.type="portgeometry"/>\n\
  <key for="port" id="d3" yfiles.type="portuserdata"/>\n\
  <key attr.name="url" attr.type="string" for="node" id="d4"/>\n\
  <key attr.name="description" attr.type="string" for="node" id="d5"/>\n\
  <key for="node" id="d6" yfiles.type="nodegraphics"/>\n\
  <key attr.name="url" attr.type="string" for="edge" id="d7"/>\n\
  <key attr.name="description" attr.type="string" for="edge" id="d8"/>\n\
  <key for="edge" id="d9" yfiles.type="edgegraphics"/>\n\
  <graph edgedefault="directed" id="G">\n')

# write nodes
for dataset in data.keys():
	# initialize variables: id, label, color, size
	id = dataset.encode("ascii","ignore")

	label = dataset.encode("ascii","ignore")
	if "name" in data[dataset].keys():
		tmp = data[dataset]["name"].encode("ascii","ignore")
		if len(tmp) <= 20 and len(tmp)<=len(label)-5:
			label = tmp
	if len(label) >= 8:
		if re.match(r".* .*",label):
			label=re.sub(" ","\n",label)
		elif re.match(r".*-.*",label):
			label=re.sub("-","-\n",label)
		#elif re.match(r".*[a-z][A-Z].*",label):
		#	label=re.sub("([a-z])([A-Z])","\1\n\2",label)

	color = "#FFFFFF"

	# LDL-2013:
	# if "type" in data[dataset].keys():
		# if data[dataset]["type"]=='lexicon':
			# color='#CCFFCC'
		# if data[dataset]["type"]=='corpus':
			# color='#99CCFF'
		# if data[dataset]["type"]=='language_description':
			# color='#FFCC99'
	
	# LDL-2014:
	type = "unknown"
	if "tags" in data[dataset].keys():
		# language description
		type = "meta"


	name_plus_tags = ""
	if "name" in data[dataset].keys(): name_plus_tags = data[dataset]["name"].encode("utf-8")
	name_plus_tags=name_plus_tags+" ["
	if "tags" in data[dataset].keys(): 
		for i in data[dataset]["tags"]:
			name_plus_tags = name_plus_tags+" \""+i.encode('utf-8')+"\""
	name_plus_tags = name_plus_tags+" ]"
	name_plus_tags = name_plus_tags.lower()

	if 'lexicon' in name_plus_tags:
		type="lexicon.lexicon"
	if 'lexical-resources' in name_plus_tags:
		type="lexicon.lexicon"
	
	if name_plus_tags.find("typology")!=-1:
		type="meta.db"
	if "name" in data[dataset].keys(): 
		if data[dataset]["name"].encode("utf-8").lower().find("dbpedia")!=-1: type="lexicon.generalKB"
		if data[dataset]["name"].encode("utf-8").lower().find("ontos")!=-1: type="lexicon.generalKB"
		if data[dataset]["name"].encode("utf-8").lower().find("asit")!=-1: type="lexicon.generalKB"
		if data[dataset]["name"].encode("utf-8").lower().find("heart failure")!=-1: type="lexicon.generalKB"
		if data[dataset]["name"].encode("utf-8").lower().find("zhishi.me")!=-1: type="lexicon.generalKB"
	if name_plus_tags.find("dbpedia")!=-1: type="lexicon.generalKB"
	if name_plus_tags.find("yago")!=-1: type="lexicon.generalKB"
	if name_plus_tags.find("thesaurus")!=-1: type="lexicon.generalKB"
	if name_plus_tags.find("vocab-mappings")!=-1: type="lexicon.generalKB"
	if name_plus_tags.find("wiktionary")!=-1: type="lexicon.lexicon"
	if name_plus_tags.find("sentiment")!=-1: type="lexicon.lexicon"
	if name_plus_tags.find("lemon")!=-1: type="lexicon.lexicon"
	if name_plus_tags.find("isocat")!=-1: type="meta.term" 
	if name_plus_tags.find("biblio")!=-1: type="meta.bib"
	if name_plus_tags.find("general ontology of linguistic description")!=-1: type="meta.term"
	if name_plus_tags.find("corpus")!=-1: type="corpus"
	if name_plus_tags.find("treebank")!=-1: type="corpus"
	if name_plus_tags.find("corpora")!=-1: type="corpus"
	if name_plus_tags.find("semanticquran")!=-1: type="corpus"
	if name_plus_tags.find("wordnet")!=-1: type="lexicon.lexicon"
	if "name" in data[dataset].keys(): 
		if data[dataset]["name"].encode("utf-8").lower().find("olia")!=-1: type="meta.term"
		if data[dataset]["name"].encode("utf-8").lower().find("lingvoj")!=-1: type="meta.term"
		if data[dataset]["name"].encode("utf-8").lower().find("gemet")!=-1: type="lexicon.generalKB"
		if data[dataset]["name"].encode("utf-8").lower()=="simple": type="lexicon.lexicon"
		if data[dataset]["name"].encode("utf-8").lower().find("lexicon")!=-1: type="lexicon.lexicon"
		if data[dataset]["name"].encode("utf-8").lower().find("the speech accent archive")!=-1: type="corpus"
		if data[dataset]["name"].encode("utf-8").lower().find("lexvo")!=-1: type="meta.term"
		if data[dataset]["name"].encode("utf-8").lower().find("lexinfo")!=-1: type="meta.term"
		if data[dataset]["name"].encode("utf-8").lower().find("glottolog")!=-1: type="meta.db"
		if data[dataset]["name"].encode("utf-8").lower().find("automated similarity judgment program lexical data")!=-1: type="meta.db"
		if data[dataset]["name"].encode("utf-8").lower().find("ietflang")!=-1: type="meta.term"
		if data[dataset]["name"].encode("utf-8").lower().find("intercontinental dictionary series")!=-1: type="lexicon.lexicon"
		if data[dataset]["name"].encode("utf-8").lower().find("yleinen suomalainen asiasanasto")!=-1: type="lexicon.generalKB"
		if data[dataset]["name"].encode("utf-8").lower().find("jrc-name")!=-1: type="lexicon.generalKB"
		if data[dataset]["name"].encode("utf-8").lower().find("world atlas of language structuctures")!=-1: type="meta.db"
		if data[dataset]["name"].encode("utf-8").lower().find("world loanword database")!=-1: type="lexicon.lexicon"
		if data[dataset]["name"].encode("utf-8").lower().find("gold")!=-1: type="meta.term"
	
	print name_plus_tags+" --> "+type
			
	# html color codes: http://html-color-codes.info/
	if type == "meta": color='#FFCC99'				# default
	if type == "meta.db": color='#C2966A'			# darker
	if type == "meta.term": color='#FFA74E'			# more intense
	if type == "meta.bib": color='#FFE6CB'			# brighter
	if type == "lexicon": color='#CCFFCC'			# default
	if type == "lexicon.lexicon": color='#8BFF8B'	# more intense
	if type == "lexicon.generalKB": color='#EEFFEE' # brighter
	if type == "corpus": color='#99CCFF'
	
	size = vertexBaseSize
	if "triples" in data[dataset].keys():
		size = float(data[dataset]["triples"])
		size = vertexBaseSize * math.pow(math.log(size+1)+1,1)

		graphml.write('\
		<node id="'+id+'">\n\
		  <data key="d4"><![CDATA['+data[dataset]["url"]+']]></data>\
		  <data key="d6">\n\
			<y:ShapeNode>\n\
			  <y:Geometry height="'+str(size)+'" width="'+str(size)+'"/>\n\
			  <y:Fill color="'+color+'" transparent="false"/>\n\
			  <y:BorderStyle color="#2222CC" type="line" width="1.0"/>\n\
			  <y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Sans" fontSize="30" fontStyle="plain" hasBackgroundColor="false" hasLineColor="false" height="53.00390625" modelName="custom" textColor="#000000" visible="true" width="81.841796875">'+label.encode("ascii","ignore")+'<y:LabelModel>\n\
				  <y:SmartNodeLabelModel distance="4.0"/>\n\
				</y:LabelModel>\n\
				<y:ModelParameter>\n\
				  <y:SmartNodeLabelModelParameter labelRatioX="0.0" labelRatioY="0.0" nodeRatioX="0.0" nodeRatioY="0.0" offsetX="0.0" offsetY="0.0" upX="0.0" upY="-1.0"/>\n\
				</y:ModelParameter>\n\
			  </y:NodeLabel>\n\
			  <y:Shape type="ellipse"/>\n\
			</y:ShapeNode>\n\
		  </data>\n\
		</node>\n')

# write edges
nr = 0
for dataset in data.keys():
	src = dataset.encode("ascii","ignore")
	if "triples" in data[dataset].keys():
		if "links" in data[dataset].keys():
			for target,wt in data[dataset]["links"].items():
				if target in data.keys():
					if "triples" in data[target].keys():
						if target in data.keys():
							s = math.log10(float(wt))
							tgt = target.encode("ascii","ignore")
							edgesize = edgeBaseSize * s
							id='e'+str(nr)
							nr = nr+1
							graphml.write('\
				<edge id="'+id+'" source="'+src+'" target="'+tgt+'">\n\
				  <data key="d9">\n\
					<y:PolyLineEdge>\n\
					  <y:Path sx="0.0" sy="0.0" tx="0.0" ty="0.0"/>\n\
					  <y:LineStyle color="#AAAAAA" type="line" width="'+str(edgesize)+'"/>\n\
					  <y:Arrows source="none" target="standard"/>\n\
					  <y:BendStyle smoothed="false"/>\n\
					</y:PolyLineEdge>\n\
				  </data>\n\
				</edge>\n')
		else:
			sys.stderr.write("no links attribute in "+dataset+"\n")
	else:
		sys.stderr.write("no triples attribute in "+dataset+"\n")
		
# finalize file
graphml.write('</graph>\
    <y:Resources/>\
</graphml>')
graphml.close()
# note that the nodes are not automatically positioned, this can be done using yEd