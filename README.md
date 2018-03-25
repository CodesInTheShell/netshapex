# netshapex
Python library to make a networkx graph from ESRI shapefile.

Reads a single shapefile (ESRI) of type point and or linestring. 

The keys are the string of their geometry coordinates.

nodes_fixed_positions is the position of each node in Decimal Degree based of the geometry attribute
of the features in the layer being read. It is essential to preserve the location of points specially
when plotting.

When reading a type LineString, nodes are automatically created in the graph.


------------------------ EXAMPLE USAGE - Reading a shapelfile--------------------------------

import networkx as nx

import matplotlib.pyplot as plt

import netshapex

G1, nodes_fixed_postions = netshapex.io.read("/path/to/shp/edge_streets.shp")

print ("=============NODES============")

print (G1.nodes(data=True))

print ("=============EDGES============")

print (G1.edges(data=True))

nx.draw_networkx(G1, nodes_fixed_postions, with_labels=True)

plt.show()

------------------------ EXAMPLE USAGE - Writing a shapelfile--------------------------------

import networkx as nx

import matplotlib.pyplot as plt

import netshapex

G2, nodes_fixed_postions = netshapex.io.read("/home/path/to/shapefile/edge_streets.shp")

schema = netshapex.getSchema("/home/path/to/shapefile/edge_streets.shp")

crs = netshapex.getCrs("/home/path/to/shapefile/edge_streets.shp")

netshapex.io.write("/home/path/to/shapefile/output_edge.shp", G2, schema, crs)



------------------------ DEPENDENCIES- -------------------------------------

  Fiona
  Networkx
  Shapely

