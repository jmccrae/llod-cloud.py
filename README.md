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

Edit the resulting graph with yed (http://www.yworks.com/en/products_yed_about.html)

	generate "organic" layout
	reformat manually
	copy/adjust legend from older diagrams
	export to SVG
	
Fix SVG export: front nodes, replace API URLs with regular datahub URLs

	xsltproc finalize-svg.xsl FILEin.svg > FILEout.svg

The modified SVG is the "official" diagram