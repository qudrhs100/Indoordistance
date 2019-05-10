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

#############################################################################




tree = ET.parse('cellspaceboundary_door.gml')
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

start_room=""
dest_room=""

class Point_make:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))

def euclidean_distance(x,y):
    return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))

def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def calculate_path():
    print("Caculatepath")


def processOK():
    global edges
    print("Caculate button is clicked")
    print(start_coord, "    ",dest_coord)
    for edge in edges:
        graph.add_edge(*edge)
    # print("FROM : ",start_room," TO : " ,dest_room)

    distance_sum=0

    canvas.create_line(start_coord[0],start_coord[1], door_accord[room_door[start_room]][0], door_accord[room_door[start_room]][1], width=2, fill="red")
    distance_sum=distance_sum+euclidean_distance(start_coord,door_accord[room_door[start_room]])

    canvas.create_line(dest_coord[0], dest_coord[1], door_accord[room_door[dest_room]][0], door_accord[room_door[dest_room]][1], width=2, fill="red")
    distance_sum = distance_sum + euclidean_distance(dest_coord, door_accord[room_door[dest_room]])

    # print(dijsktra(graph, room_door[start_room], room_door[dest_room]))
    PATH=dijsktra(graph, room_door[start_room], room_door[dest_room])
    for i,v in enumerate(PATH):
        if i>len(dijsktra(graph, room_door[start_room], room_door[dest_room]))-2:continue
        canvas.create_line(door_and_corner[PATH[i]][0], door_and_corner[PATH[i]][1], door_and_corner[PATH[i+1]][0],
                           door_and_corner[PATH[i + 1]][1], width=2, fill="red")
        distance_sum=distance_sum+euclidean_distance(door_and_corner[PATH[i]],door_and_corner[PATH[i+1]])

    message = tkinter.Message(window, text="FROM : "+start_room + " TO : " +dest_room, width=400, relief="solid")
    message1 = tkinter.Message(window, text="Sum of Length : " + str(distance_sum), width=400, relief="solid")
    message.pack()
    message1.pack()




def visibility():

    line_segment=[]
    for i in total_line:
        for j in range(int(len(i)/2)-1):
            line_segment.append(((i[j*2],i[j*2+1]),(i[j*2+2],i[j*2+3])))

    corner_count=0
    for i in enumerate(total_line):
        temp=i[1]
        temp.append(i[1][2])
        temp.append(i[1][3])
        for j in range(len(temp)):
            if j%2==1:continue
            if j+6>len(i[1]):continue
            A1 = (float(total_line[i[0]][j]),float(total_line[i[0]][j+1]))
            B1 = (float(total_line[i[0]][j+2]), float(total_line[i[0]][j + 3]))
            C1 = (float(total_line[i[0]][j+4]), float(total_line[i[0]][j + 5]))
            A2= (B1[0]-A1[0],B1[1]-A1[1])
            B2 = (C1[0] - B1[0], C1[1] - B1[1])
            # print(angle_between(A2, B2))
            if(angle_between(A2, B2)<180):
                # canvas.create_oval(B1[0], B1[1], B1[0], B1[1], width=8,outline="green")
                corner_accord["CORNER"+str(corner_count)]=(B1[0], B1[1])
                door_and_corner["CORNER"+str(corner_count)]=(B1[0], B1[1])
                corner_count+=1

    for i in list(itertools.combinations(door_and_corner, 2)):
        test=[]
        Door_A = Point_make(float(door_and_corner[i[0]][0]),float(door_and_corner[i[0]][1]))
        Door_B = Point_make(float(door_and_corner[i[1]][0]),float(door_and_corner[i[1]][1]))
        cnt =0
        for j in line_segment:
            Line_A = Point_make(float(j[0][0]),float(j[0][1]))
            Line_B = Point_make(float(j[1][0]),float(j[1][1]))
            if intersect(Door_A,Door_B,Line_A,Line_B)==True:
                cnt+=1
                test.append((Door_A,Door_B,Line_A,Line_B))
        if cnt<3:
            # canvas.create_line(Door_A.x, Door_A.y, Door_B.x, Door_B.y, width=2, fill="red")
            temp_A=(Door_A.x,Door_A.y)
            temp_B=(Door_B.x,Door_B.y)
            edges.append((i[0],i[1],euclidean_distance(temp_A,temp_B)))




def click(event):
    global total_click
    global start_coord
    global dest_coord
    global start_room
    global dest_room
    total_click=total_click+1
    if total_click>2:
        return
    if total_click==1:
        for key, value in cellspace_accord.items():
            point = Point(event.x, event.y)
            start_coord=(event.x, event.y)
            polygon=Polygon(value)
            if polygon.contains(point)==True:
                start_room=key

    if total_click==2:
        for key, value in cellspace_accord.items():
            point = Point(event.x, event.y)
            dest_coord=(event.x, event.y)
            polygon = Polygon(value)
            if polygon.contains(point)==True:
                dest_room=key




    print("Button click", event.x, event.y)
    # print (total_click)
    canvas.create_oval(event.x, event.y, event.x,  event.y, width=5, fill="#ff0000")
    window.mainloop()


def main():
    btn = Button(window, text="Calculate", command=processOK,bg='yellow')
    canvas.bind("<Button-1>", click)


    for i in root.findall("./{http://www.opengis.net/indoorgml/1.0/core}primalSpaceFeatures/{http://www.opengis.net/indoorgml/1.0/core}PrimalSpaceFeatures/{http://www.opengis.net/indoorgml/1.0/core}cellSpaceMember/{http://www.opengis.net/indoorgml/1.0/core}CellSpace"):
        CS_gml_id=i.get('{http://www.opengis.net/gml/3.2}id')
        # print(i.find('{http://www.opengis.net/indoorgml/1.0/core}partialboundedBy'))
        if i.find('{http://www.opengis.net/indoorgml/1.0/core}partialboundedBy')!=None:
            room_door[CS_gml_id]=i.find('{http://www.opengis.net/indoorgml/1.0/core}partialboundedBy').get('{http://www.w3.org/1999/xlink}href')[1:]
        list=[]
        list_set=[]
        for j in i.findall("./{http://www.opengis.net/indoorgml/1.0/core}cellSpaceGeometry/{http://www.opengis.net/indoorgml/1.0/core}Geometry2D/{http://www.opengis.net/gml/3.2}Polygon/{http://www.opengis.net/gml/3.2}exterior/{http://www.opengis.net/gml/3.2}LinearRing/{http://www.opengis.net/gml/3.2}pos"):
            words=j.text.split()
            list.append(str(float(words[0])))
            list.append(str(float(words[1])))
            input = (float(words[0]),float(words[1]))
            list_set.append(input)
        canvas.create_polygon(list, outline='black', fill='ivory3', width=2)
        total_line.append(list)
        cellspace_accord[CS_gml_id]=list_set


    for i in root.findall("./{http://www.opengis.net/indoorgml/1.0/core}primalSpaceFeatures/{http://www.opengis.net/indoorgml/1.0/core}PrimalSpaceFeatures/{http://www.opengis.net/indoorgml/1.0/core}cellSpaceBoundaryMember/{http://www.opengis.net/indoorgml/1.0/core}CellSpaceBoundary"):
        gml_id=i.get('{http://www.opengis.net/gml/3.2}id')
        if gml_id.find("REVERSE")!= -1 : continue ##Reverse가 들어가 있을 경우 continue
        sum_x = 0
        sum_y = 0
        for j in i.findall("{http://www.opengis.net/indoorgml/1.0/core}cellSpaceBoundaryGeometry/{http://www.opengis.net/indoorgml/1.0/core}geometry2D/{http://www.opengis.net/gml/3.2}LineString/{http://www.opengis.net/gml/3.2}pos"):
            words=j.text.split()
            sum_x+=float(words[0])
            sum_y+=float(words[1])
        canvas.create_image(sum_x/2-15, sum_y/2-15, image=img, anchor=NW)
        total_door.append((sum_x/2,sum_y/2))
        door_accord[gml_id]=(sum_x/2,sum_y/2)
        door_and_corner[gml_id] = (sum_x/2,sum_y/2)


    visibility()


    # for key, value in cellspace_accord.items():
    #     print(key, value)
    # print(edges)
    plt.show()
    canvas.pack()
    btn.pack()
    window.mainloop()

if __name__ == "__main__":
    main()