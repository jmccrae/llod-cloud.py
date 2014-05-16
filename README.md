Linguistic Linked Open Data Cloud
=================================

Code for generating linguistic linked open data image

Example image
-------------

![LLOD Cloud](https://raw.github.com/jmccrae/llod-cloud.py/master/llod-cloud.png)


Requirements
------------

Requires Python and [graph_tool](http://graph-tool.skewed.de)

Running
-------

Download the data using

    python datahub.py

Generate the graph with

    python llod-cloud.graphml.py 

Load the resulting graph with yed 

	generate "organic" layout
	reformat manually
	export to SVG
	
Fix SVG export: move edges to the background

	xsltproc fixGraphmlSVG.xsl FILEin.svg > FILEout.svg

The modified SVG is the "official" diagram
