import xml.etree.ElementTree as ET
import tkinter
import matplotlib.pyplot as plt
import itertools
import numpy as np
from math import *
from collections import defaultdict
from shapely.geometry import Point,MultiLineString
from shapely.geometry.polygon import Polygon
from shapely.geometry import LineString
from tkinter import *
from PIL import ImageTk, Image
import shapely.affinity as affinity
from shapely.ops import linemerge, unary_union, polygonize

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
# tree = ET.parse('data/313-4F-2D-190612.gml')
tree = ET.parse('data/Handmade_313.gml')
root = tree.getroot()
window = tkinter.Tk()

window.title("Indoor Distance")
canvas = tkinter.Canvas(window, width=1000, height=500)
img = ImageTk.PhotoImage(Image.open("Door.png"))

total_click = 0
total_line=[]
corridor_line=[]##Corridor의 cellspace set
door_line=[]
total_door=[]
start_coord=()
dest_coord=()
room_door={}##Room<->Door duality 관계확인

cellspace_accord={}##cellspace 와 각각의 좌표


door_accord={}##door들과 각각의 좌표값
corner_accord={}##coner들과 각각의 좌표값
grid_accord={}##grid_point들 각각의 좌표값
door_and_corner={}##door와 corner(Graph생성에 포함되어야 한는 node)들과 그의 좌표

vertical_line=[]##문에 대한 vertical line에 대한 배열

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

def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))

def draw_vertical():
    SUM=[]
    for i in corridor_line:
        print(i)
    for i in vertical_line:
        for j in corridor_line:
            # print(i.intersection(j))
            if i.intersection(j).type=="Point":continue
            # print(i.intersection(j).type)
            temp_linestring=LineString(i.intersection(j))
            little_scale_Linestring = affinity.scale(temp_linestring, xfact=1.3, yfact=1.3)
            # print(tuple(little_scale_Linestring.coords))
            SUM.append(tuple(little_scale_Linestring.coords))
            # for k in little_scale_Linestring.coords:
            #     print (k)

    for i in corridor_line:
        SUM.append(tuple(i.coords))
    # print(corridor_line)
    MULT = MultiLineString(SUM)
    borders = unary_union(MULT)
    polygons = polygonize(borders)
    for p in polygons:
        # print(list(p.centroid.coords))
        centroid=list(p.centroid.coords)

        canvas.create_polygon(list(p.exterior.coords), outline='black', fill='ivory3', width=2)
        canvas.create_oval(centroid[0][0], centroid[0][1], centroid[0][0], centroid[0][1], width=5, outline="green")
    window.mainloop()

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

class Point_make:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def calc_min_max(POINT):
    global MIN_X,MAX_X,MIN_Y,MAX_Y
    # print(POINT[0],"    ",POINT[1])
    MIN_X=min(POINT[0],MIN_X)
    MAX_X=max(POINT[0],MAX_X)
    MIN_Y=min(POINT[1],MIN_Y)
    MAX_Y=max(POINT[1],MAX_Y)

def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))

def euclidean_distance(x,y):
    return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))


def calculate_path():
    print("Caculatepath")




def processOK():
    global edges
    global start_coord
    global dest_coord
    print("Caculate button is clicked")
    # print(edges)
    for edge in edges:
        graph.add_edge(*edge)


    distance_sum=0


    PATH=dijsktra(graph,start_coord ,dest_coord)
    # print(PATH)
    for i,v in enumerate(PATH):
        if i>len(PATH)-2:continue
        canvas.create_line(grid_accord[PATH[i]][0], grid_accord[PATH[i]][1], grid_accord[PATH[i+1]][0],
                           grid_accord[PATH[i + 1]][1], width=2, fill="red")
        distance_sum=distance_sum+euclidean_distance(grid_accord[PATH[i]],grid_accord[PATH[i+1]])
    message1 = tkinter.Message(window, text="Sum of Length : " + str(distance_sum), width=400, relief="solid")
    message2 = tkinter.Message(window, text="# of Turns  : " + str(distance_sum), width=400, relief="solid")
    message1.pack()
    message2.pack()


def click(event):
    global total_click
    global start_coord
    global dest_coord
    total_click=total_click+1
    min_distance=99999
    for i in range(1,77):
        print(i,end=' ')
    if total_click>2:
        return
    if total_click==1:
        for key,value in grid_accord.items():
            if euclidean_distance(value,(event.x,event.y))<min_distance:
                min_distance=euclidean_distance(value,(event.x,event.y))
                start_coord=key

    if total_click==2:
        for key,value in grid_accord.items():
            if euclidean_distance(value,(event.x,event.y))<min_distance:
                min_distance = euclidean_distance(value, (event.x, event.y))
                dest_coord=key

    # print (start_coord, dest_coord)




    print("Button click", event.x, event.y)
    # print (total_click)
    canvas.create_oval(event.x, event.y, event.x,  event.y, width=5, outline="red")
    window.mainloop()


def main():
    scale_x=1
    scale_y=1
    btn = Button(window, text="Calculate", command=processOK,bg='yellow')
    canvas.bind("<Button-1>", click)

    for i in root.findall("./{http://www.opengis.net/indoorgml/1.0/core}primalSpaceFeatures/{http://www.opengis.net/indoorgml/1.0/core}PrimalSpaceFeatures/{http://www.opengis.net/indoorgml/1.0/core}cellSpaceMember/{http://www.opengis.net/indoorgml/1.0/core}CellSpace"):
        CS_gml_id=i.get('{http://www.opengis.net/gml/3.2}id')
        CS_name =i.find('{http://www.opengis.net/gml/3.2}name').text
        if i.find('{http://www.opengis.net/indoorgml/1.0/core}partialboundedBy')!=None:
            room_door[CS_gml_id]=i.find('{http://www.opengis.net/indoorgml/1.0/core}partialboundedBy').get('{http://www.w3.org/1999/xlink}href')[1:]
        list=[]
        list_set=[]
        for j in i.findall("./{http://www.opengis.net/indoorgml/1.0/core}cellSpaceGeometry/{http://www.opengis.net/indoorgml/1.0/core}Geometry2D/{http://www.opengis.net/gml/3.2}Polygon/{http://www.opengis.net/gml/3.2}exterior/{http://www.opengis.net/gml/3.2}LinearRing/{http://www.opengis.net/gml/3.2}pos"):
            words=j.text.split()
            list.append(str(float(words[0])*scale_x+20))
            list.append(str(float(words[1])*scale_y+20))
            FOR_MIN_MAX=((float(words[0])*scale_x+20),(float(words[1])*scale_y+20))
            calc_min_max(FOR_MIN_MAX)
            input = (float(words[0])*scale_x+20,float(words[1])*scale_y+20)
            list_set.append(input)
        canvas.create_polygon(list, outline='black', fill='ivory3', width=2)
        # print(list)
        if CS_name.find("Corridor")!=-1:
            # print(list_set)
            corridor_line.append(LineString(list_set))
        else:
            total_line.append(list)
        cellspace_accord[CS_gml_id]=list_set


    for i in root.findall("./{http://www.opengis.net/indoorgml/1.0/core}primalSpaceFeatures/{http://www.opengis.net/indoorgml/1.0/core}PrimalSpaceFeatures/{http://www.opengis.net/indoorgml/1.0/core}cellSpaceBoundaryMember/{http://www.opengis.net/indoorgml/1.0/core}CellSpaceBoundary"):
        gml_id=i.get('{http://www.opengis.net/gml/3.2}id')
        if gml_id.find("REVERSE")!= -1 : continue ##Reverse가 들어가 있을 경우 continue

        sum_x = 0
        sum_y = 0
        DOOR=[]
        for j in i.findall("{http://www.opengis.net/indoorgml/1.0/core}cellSpaceBoundaryGeometry/{http://www.opengis.net/indoorgml/1.0/core}geometry2D/{http://www.opengis.net/gml/3.2}LineString/{http://www.opengis.net/gml/3.2}pos"):
            words=j.text.split()
            DOOR.append([float(words[0])*scale_x+20,float(words[1])*scale_y+20])
            sum_x+=float(words[0])*scale_x+20
            sum_y+=float(words[1])*scale_y+20
        total_door.append((sum_x/2,sum_y/2))
        door_accord[gml_id]=(sum_x/2,sum_y/2)
        door_line.append(LineString([(DOOR[0][0], DOOR[0][1]),(DOOR[1][0], DOOR[1][1])]))
        canvas.create_line(DOOR[0][0], DOOR[0][1], DOOR[1][0], DOOR[1][1], width=10, fill="blue")
        ##Door에서 vertical 한 line 생성

        DOOR_Linestring = LineString([(DOOR[0][0], DOOR[0][1]),(DOOR[1][0], DOOR[1][1])])##DOOR를 Linestring으로 변환
        # print(DOOR[0][0], DOOR[0][1], DOOR[1][0], DOOR[1][1])
        # for i in DOOR_Linestring.coords:
        #     print (i)
        # print(DOOR_Linestring.coords[0],DOOR_Linestring.coords[1])
        # print("------------------------------------------------------------------------------------------")

        Rotate_Linestring = affinity.rotate(DOOR_Linestring,90)##90도 수직 시킨 길이

        Rotate_Linestring = affinity.scale(Rotate_Linestring, xfact = 100, yfact= 100)#100배씩 해줌 (Door 수직 한거 길이 100배)
        vertical_line.append(Rotate_Linestring)
        # canvas.create_line(Rotate_Linestring.coords[0][0], Rotate_Linestring.coords[0][1], Rotate_Linestring.coords[1][0], Rotate_Linestring.coords[1][1], width=3, fill="green")
        ##Door에서 vertical 한 line 생성
        door_and_corner[gml_id] = (sum_x/2,sum_y/2)

    for key,value in room_door.items():
        if(value.find("-REVERSE")!=-1):
            room_door[key]=value[0:value.find("-REVERSE")]

    # visibility()

    plt.show()
    canvas.pack()
    btn.pack()
    draw_vertical()

    window.mainloop()

if __name__ == "__main__":
    main()