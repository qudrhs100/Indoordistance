import xml.etree.ElementTree as ET
import tkinter
import matplotlib.pyplot as plt
import itertools
import numpy as np
from math import *
from collections import defaultdict
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from tkinter import *
from PIL import ImageTk, Image


class Graph():
    def __init__(self):
        """
        self.edges is a dict of all possible next nodes
        e.g. {'X': ['A', 'B', 'C', 'E'], ...}
        self.weights has all the weights between two nodes,
        with the two nodes as a tuple as the key
        e.g. {('X', 'A'): 7, ('X', 'B'): 2, ...}
        """
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight

def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))

def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path

###############################################################################


# tree = ET.parse('victoriaAirport_IndoorGML_v304demo_4326_zm.gml')
tree = ET.parse('victoriaAirport_IndoorGML_v304.gml')
root = tree.getroot()
window = tkinter.Tk()
window.title("Indoor Distance")
canvas = tkinter.Canvas(window, width=500, height=500)
img = ImageTk.PhotoImage(Image.open("Door.png"))
total_click = 0
total_line=[]
total_door=[]
start_coord=()
dest_coord=()
room_door={}##Room<->Door duality 관계확인

cellspace_accord={}##cellspace 와 각각의 좌표

door_accord={}##door들과 각각의 좌표값
corner_accord={}##coner들과 각각의 좌표값
door_and_corner={}##door와 corner(Graph생성에 포함되어야 한는 node)들과 그의 좌표

graph = Graph()##최소거리를 계산하기 위한 그래프
edges = []##그래프의 edges

##
MIN_X=999999
MAX_X=-999999
MIN_Y=999999
MAX_Y=-999999
##Grid를 만들기 위한 min x,y

start_room=""
dest_room=""






def main():
    # canvas.bind("<Button-1>", click)

    for i in root.findall("./{http://www.opengis.net/indoorgml/1.0/core}primalSpaceFeatures/{http://www.opengis.net/indoorgml/1.0/core}PrimalSpaceFeatures/{http://www.opengis.net/indoorgml/1.0/core}cellSpaceMember/{http://indoorgml.net/extensions/PSExt}PublicSafetyRoom"):
        # CS_gml_id=i.get('{http://www.opengis.net/gml/3.2}id')
        # print(CS_gml_id)

        # print(i.find('{http://www.opengis.net/indoorgml/1.0/core}partialboundedBy'))
        # if i.find('{http://www.opengis.net/indoorgml/1.0/core}partialboundedBy')!=None:
        #     room_door[CS_gml_id]=i.find('{http://www.opengis.net/indoorgml/1.0/core}partialboundedBy').get('{http://www.w3.org/1999/xlink}href')[1:]
        list=[]
        list_set=[]
        for j in i.findall("./{http://www.opengis.net/indoorgml/1.0/core}cellSpaceGeometry/{http://www.opengis.net/indoorgml/1.0/core}Geometry3D/{http://www.opengis.net/gml/3.2}Solid/{http://www.opengis.net/gml/3.2}exterior/{http://www.opengis.net/gml/3.2}Shell"
                           "/{http://www.opengis.net/gml/3.2}surfaceMember/{http://www.opengis.net/gml/3.2}CompositeSurface"):
            for k in j.findall("./{http://www.opengis.net/gml/3.2}surfaceMember/{http://www.opengis.net/gml/3.2}Surface/{http://www.opengis.net/gml/3.2}patches/{http://www.opengis.net/gml/3.2}PolygonPatch/{http://www.opengis.net/gml/3.2}exterior/{http://www.opengis.net/gml/3.2}LinearRing/{http://www.opengis.net/gml/3.2}posList"):
                # print(k.text)
                words=k.text.split()
                # print(len(words))
                for l in range(0,len(words)-1,3):
                    # print(l)
                    list.append(str(float(words[l])))
                    list.append(str(float(words[l+1])))
                    input = (float(words[l]),float(words[l+1]))
                    print(input)
                    list_set.append(input)
                canvas.create_polygon(list, outline='black', fill='ivory3', width=2)
        # total_line.append(list)
        # cellspace_accord[CS_gml_id]=list_set


    # for i in root.findall("./{http://www.opengis.net/indoorgml/1.0/core}primalSpaceFeatures/{http://www.opengis.net/indoorgml/1.0/core}PrimalSpaceFeatures/{http://www.opengis.net/indoorgml/1.0/core}cellSpaceBoundaryMember/{http://www.opengis.net/indoorgml/1.0/core}CellSpaceBoundary"):
    #     gml_id=i.get('{http://www.opengis.net/gml/3.2}id')
    #     if gml_id.find("REVERSE")!= -1 : continue ##Reverse가 들어가 있을 경우 continue
    #     sum_x = 0
    #     sum_y = 0
    #     for j in i.findall("{http://www.opengis.net/indoorgml/1.0/core}cellSpaceBoundaryGeometry/{http://www.opengis.net/indoorgml/1.0/core}geometry2D/{http://www.opengis.net/gml/3.2}LineString/{http://www.opengis.net/gml/3.2}pos"):
    #         words=j.text.split()
    #         sum_x+=float(words[0])
    #         sum_y+=float(words[1])
    #     canvas.create_image(sum_x/2-15, sum_y/2-15, image=img, anchor=NW)
    #     total_door.append((sum_x/2,sum_y/2))
    #     door_accord[gml_id]=(sum_x/2,sum_y/2)
    #     door_and_corner[gml_id] = (sum_x/2,sum_y/2)

    #
    # for key, value in cellspace_accord.items():
    #     print(key, value)

    # for key, value in door_and_corner.items():
    #     print(key, value)
    # print(edges)
    plt.show()
    canvas.pack()
    window.mainloop()

if __name__ == "__main__":
    main()