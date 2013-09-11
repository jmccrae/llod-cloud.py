from graph_tool.all import *
import json
import math
import cairo
import datetime

edgeBaseSize=3
vertexBaseSize=100
canvas=4000

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,canvas,canvas)
ctx = cairo.Context(surface)

data = json.load(open("llod-cloud.json"))

g = Graph()

label = g.new_vertex_property("string")
size = g.new_vertex_property("float")
edgesize = g.new_edge_property("float")
nodes = {}
edgecount= {}

for dataset in data.keys():
  v = g.add_vertex()
  nodes[dataset] = v
  label[v] = dataset
  size[v] = vertexBaseSize

for dataset in data.keys():
  for target,wt in data[dataset]["links"].items():
    s = math.log10(float(wt))
    e = g.add_edge(nodes[dataset],nodes[target])
    edgesize[e] = edgeBaseSize * s
  if "triples" in data[dataset].keys():
    s = float(data[dataset]["triples"])
    s = vertexBaseSize * math.pow(math.log10(s+1)+1,0.4)
    size[nodes[dataset]] = s

pos = sfdp_layout(g,p=7)
# .67 .84 .90
cairo_draw(g,pos,ctx,vertex_text=label, vertex_size=size, vertex_pen_width=8.0, vertex_color=[0.2,0.2,0.9,1.0], vertex_font_size=52,vertex_fill_color=[1.0,1.0,1.0,1.0], vertex_text_color="black",vertex_text_position=-2, edge_pen_width=edgesize, edge_marker_size=40,fit_view=True,vertex_font_family="sans",vertex_font_weight=cairo.FONT_WEIGHT_BOLD)

ctx.move_to(canvas*0.02,canvas*0.95)
ctx.set_font_size(72)
ctx.show_text("Linguistic Linked Open Data Cloud")
ctx.move_to(canvas*0.13,canvas*0.97)
ctx.show_text(datetime.datetime.now().strftime("%B %Y"))

surface.write_to_png("llod-cloud.png")
