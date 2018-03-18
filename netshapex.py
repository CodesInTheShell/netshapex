# ----------------------------------------------------------------#                                         
#     _____                                             _____     #
#   || 0100 |\                                       /| 0100 ||   #
#   || 0100_|/ -------  Codes_In_The_Shell  -------- \| 0001 ||   #
#                                                                 #
#-----------------------------------------------------------------#

# ================================= LICENSE ====================================
#
# MIT License
#
# Copyright (c) 2018 Dante Abidin Jr
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ================================= LICENSE ====================================

# =========================== DEPENDENCIES / REQUIREMENTS ======================
# pip install fiona         
# pip install networkx
# pip install shapely
# =========================== DEPENDENCIES / REQUIREMENTS ======================


import fiona
from fiona.crs import from_epsg
import networkx as nx
from shapely.geometry import Point, mapping, LineString

class io():
    """"
    Class for reading and writing shapefile (ESRI) and networkx graph vice versa. 
    Convert .shp to a networkx graph. 

    """

    def read(path):
        """
        Reads a single shapefile (ESRI) of type point and or linestring. 
        The keys are the string of their geometry coordinates.

        PARAMETER(S):

        : path : path to the .shp file. (e.i. C:\\path\to\line_street.shp)

        RETURN(S):

        : G : Networkx Graph()

        : nodes_fixed_positions : Position of each node in Decimal Degree based of the geometry attribute
            of the features in the layer being read. It is essential to preserve the location of points.
            (e.i. 
                (120.90432974785224, 14.391880515315119) for nodes
                (120.90432974785224, 14.391880515315119)', '(120.90420818465601, 14.392083151914841) for edges
            )

        EXAMPLE:

        To make a graph from .shp

            import netshapex

            G1, nodes_fixed_postions = netshapex.io.read("line_streets.shp")
            G2, nodes_fixed_postions = netshapex.io.read("point_poles.shp")

            print(G1.edges(data=True)
            print(G2.nodes(data=True)

            # To draw or plot
            import matplotlib.pyplot as plt
            nx.draw_networkx(G1, nodes_fixed_postions, with_labels=True)
            nx.draw_networkx(G2, nodes_fixed_postions, with_labels=True)
            plt.show()

        """

        G = nx.Graph()

        path = path

        with fiona.open(path) as shpfile:

            if (shpfile[0]['geometry']['type']) == "LineString":

                nodes_fixed_postions = {}

                count = 0

                for s in shpfile:

                    nodeid = str(list(s['geometry']['coordinates'])[0])

                    nodes_fixed_postions[nodeid] = list(s['geometry']['coordinates'])[0]
                    id_for_edge_1 = nodeid

                    nodeid = str(list(s['geometry']['coordinates'])[1])

                    nodes_fixed_postions[nodeid] = list(s['geometry']['coordinates'])[1]
                    id_for_edge_2 = nodeid

                    G.add_edge(id_for_edge_1, id_for_edge_2, geom=s)

                return G, nodes_fixed_postions

            if (shpfile[0]['geometry']['type']) == "Point":

                nodes_fixed_postions = {}

                for s in shpfile:

                    nodeid = str(s['geometry']['coordinates'])
                    nodes_fixed_postions[nodeid] = s['geometry']['coordinates']

                    G.add_node(nodeid, geom=s)

                return G, nodes_fixed_postions 

    def write(path, G, schema, crs):
        """
        Write a shapefile (ESRI .shp) from a given network graph.

        PARAMETER(S):

        : path : Path where to create the .shp file. (e.i. C:\\path\to\output.shp)

        : G : The graph to convert to a .shp file.

        : schema : The schema for the attributes of the output .shp file. 
            Schema of source .shp file can be copied. 

                Example to copy the a schema.

                    schema = netshapex.getSchema(C:\\path\to\source.shp)

            If no schema where provided. This will use the defualt schema, refer to the code below.
            Schema can also be created. If creating .shp file without any source schema, you should
            create the schema according to what you want to include and is available in you graph object. 
            See fiona documentation for more information on creating schema.

                Example of creating you own schema

                 schema = {'geometry': 'Point',
                            'properties': {'id': 'float:16',}
                            }

        : crs : Coordinate reference system to use. Defualt is EPSG: 4326. 
            Example to copy the crs of a source.shp file.

                crs = netshapex.getCrs(C:\\path\to\source.shp)

        RETURN(S):

        : Generate .shp file in the provided path argument:

        EXAMPLE(S):

        import netshapex

        G1, nodes_fixed_postions = netshapex.io.read("/home/source.shp")

        schema = netshapex.getSchema("/home/source.shp")
        crs = netshapex.getCrs("/home/source.shp")

        netshapex.io.write("/home/output_edges.shp", G1, schema, crs)
        """

        path = path

        G = G

        if not crs:
            crs = from_epsg(4326)
        else:
            crs = crs

        nodes_data = G.nodes(data=True)
        edges_data = G.edges(data=True)

        # Getting the geometry type
        if edges_data:

            for n in edges_data:

                geom_type = n[2]['geom']['geometry']['type']
                
                break
        else:
            for n in nodes_data:
                geom_type = n[1]['geom']['geometry']['type']
                break

        # Assigning schema. If schema is not provided, use the default schema below.
        if not schema:
            schema = {'geometry': geom_type,
                        'properties': {'id': 'float:16',}
                        }
        else:
            schema = schema
            
        # Generate a Point layer if the geometry type is a Point
        if geom_type == 'Point':           

            # Making a new .shp file as the output.
            with fiona.open(path, 'w', crs=crs, schema=schema, driver="ESRI Shapefile") as shpfile:

                for n in nodes_data:
                    
                    point = Point(n[1]['geom']['geometry']['coordinates'])

                    shpfile.write({
                                    'geometry': mapping(point),
                                    'properties': n[1]['geom']['properties']
                                    })

        # Generate a LineString layer if the geometry type is a LineString
        if geom_type == 'LineString':

            with fiona.open(path, 'w', crs=crs, schema=schema, driver="ESRI Shapefile") as shpfile:

                for e in edges_data:
                    
                    line = LineString(e[2]['geom']['geometry']['coordinates'])

                    shpfile.write({
                                    'geometry': mapping(line),
                                    'properties': e[2]['geom']['properties']
                                    })


####################### BEGIN SECTION FOR HELPER FUNCTIONS ##########################

def getSchema(path):
    """
    Get the schema of a shapefile as a basis to write an output shapefile.

    PARAMETER(S)

    : path : Path to the .shp file where to copy the schema.

    RETURN(S)

    : schema :  The schema from source .shp

    """

    path = path

    with fiona.open(path) as shpfile:

        schema = shpfile.schema.copy()

        return schema

def getCrs(path):
    """
    Gets the crs of the given .shp file.
    
    PARAMETER(S)

    : path : Path to the .shp file where to copy the crs.

    RETURN(S)

    : crs :  The crs from source .shp
    """

    path = path

    with fiona.open(path) as shpfile:

        crs = shpfile.crs

        return crs

####################### END SECTION FOR HELPER FUNCTIONS ##########################













