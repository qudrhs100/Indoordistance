import xml.etree.ElementTree as ET
import tkinter
import matplotlib.pyplot as plt
import networkx as nx
import itertools
import numpy as np

from tkinter import *
from PIL import ImageTk, Image


tree = ET.parse('cellspaceboundary_door.gml')
root = tree.getroot()
window = tkinter.Tk()
window.title("Indoor Distance")
canvas = tkinter.Canvas(window, width=500, height=500)
img = ImageTk.PhotoImage(Image.open("Door.png"))
total_click = 0

total_point=[]
total_line=[]
total_door=[]
G = nx.Graph()

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))

def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def calculate_path():
    print("Caculatepath")

def processOK():
    print("Caculate button is clicked")

def remove_duplication():
    global total_door
    total_door = list(set(total_door))

def visibility():

    line_segment=[]
    for i in total_line:
        for j in range(int(len(i)/2)-1):
            # print (j)
            # print (j,j+1,j+2,j+3)
            # print(i[j*2],i[j*2+1],"---->",i[j*2+2],i[j*2+3])
            line_segment.append(((i[j*2],i[j*2+1]),(i[j*2+2],i[j*2+3])))
    for i in total_door:
        print(i)
    print("Combinataion")
    for i in list(itertools.combinations(total_door, 2)):
        # print (i)
        test=[]

        Door_A = Point(float(i[0][0]),float(i[0][1]))
        Door_B = Point(float(i[1][0]),float(i[1][1]))
        cnt =0
        for j in line_segment:
            Line_A = Point(float(j[0][0]),float(j[0][1]))
            Line_B = Point(float(j[1][0]),float(j[1][1]))
            # print(intersect(Door_A,Door_B,Line_A,Line_B))
            if intersect(Door_A,Door_B,Line_A,Line_B)==True:
                cnt+=1
                test.append((Door_A,Door_B,Line_A,Line_B))

        if cnt==2:
            canvas.create_line(Door_A.x, Door_A.y, Door_B.x, Door_B.y, width=2, fill="red")

        # if len(test)==2:
        #     for i in test:
        #         canvas.create_line(i[0].x, i[0].y,i[1].x,i[1].y,width=2,fill="red")
        #         canvas.create_line(i[2].x, i[2].y, i[3].x, i[3].y, width=2, fill="blue")

        print(cnt)
        print("---------------------")





def click(event):
    global total_click
    total_click=total_click+1
    if total_click==2:
        calculate_path()
    if total_click>2:
        return
    print("Button click", event.x, event.y)
    print (total_click)
    canvas.create_oval(event.x, event.y, event.x,  event.y, width=5, fill="#ff0000")
    window.mainloop()


def main():
    btn = Button(window, text="Calculate", command=processOK,bg='yellow')
    canvas.bind("<Button-1>", click)
    for i in root.findall("./{http://www.opengis.net/indoorgml/1.0/core}primalSpaceFeatures/{http://www.opengis.net/indoorgml/1.0/core}PrimalSpaceFeatures/{http://www.opengis.net/indoorgml/1.0/core}cellSpaceMember/{http://www.opengis.net/indoorgml/1.0/core}CellSpace/{http://www.opengis.net/indoorgml/1.0/core}cellSpaceGeometry/{http://www.opengis.net/indoorgml/1.0/core}Geometry2D/{http://www.opengis.net/gml/3.2}Polygon/{http://www.opengis.net/gml/3.2}exterior/{http://www.opengis.net/gml/3.2}LinearRing"):
        list=[]
        for j in i.findall("./{http://www.opengis.net/gml/3.2}pos"):
            words=j.text.split()
            list.append(str(float(words[0])))
            list.append(str(float(words[1])))
            input = Point(float(words[0]),float(words[1]))
            total_point.append(input)
        canvas.create_polygon(list, outline='black', fill='ivory3', width=2)
        total_line.append(list)
    ##Cellspace

    for i in root.findall("./{http://www.opengis.net/indoorgml/1.0/core}primalSpaceFeatures/{http://www.opengis.net/indoorgml/1.0/core}PrimalSpaceFeatures/{http://www.opengis.net/indoorgml/1.0/core}cellSpaceBoundaryMember/{http://www.opengis.net/indoorgml/1.0/core}CellSpaceBoundary/{http://www.opengis.net/indoorgml/1.0/core}cellSpaceBoundaryGeometry/{http://www.opengis.net/indoorgml/1.0/core}geometry2D/{http://www.opengis.net/gml/3.2}LineString"):
        sum_x=0
        sum_y=0
        for j in i.findall("./{http://www.opengis.net/gml/3.2}pos"):
            words=j.text.split()
            sum_x+=float(words[0])
            sum_y+=float(words[1])
        canvas.create_image(sum_x/2-15, sum_y/2-15, image=img, anchor=NW)
        total_door.append((sum_x/2,sum_y/2))
    ##Cellspaceboundary

    # for i in root.findall("./{http://www.opengis.net/indoorgml/1.0/core}multiLayeredGraph/{http://www.opengis.net/indoorgml/1.0/core}MultiLayeredGraph/{http://www.opengis.net/indoorgml/1.0/core}spaceLayers/{http://www.opengis.net/indoorgml/1.0/core}spaceLayerMember/{http://www.opengis.net/indoorgml/1.0/core}SpaceLayer/{http://www.opengis.net/indoorgml/1.0/core}nodes"):
    #     for j in i.findall("./{http://www.opengis.net/indoorgml/1.0/core}stateMember"):
    #         # print(j.find("./{http://www.opengis.net/indoorgml/1.0/core}State/{http://www.opengis.net/gml/3.2}name").text[0])
    #         if j.find("./{http://www.opengis.net/indoorgml/1.0/core}State/{http://www.opengis.net/gml/3.2}name").text[0]!='D':continue
    #         words=j.find("./{http://www.opengis.net/indoorgml/1.0/core}State/{http://www.opengis.net/indoorgml/1.0/core}geometry/{http://www.opengis.net/gml/3.2}Point/{http://www.opengis.net/gml/3.2}pos").text.split()
    #         # print(words)
    #         canvas.create_image(float(words[0])-15, float(words[1])-15, image=img, anchor=NW)
    #         total_door.append((float(words[0]),float(words[1])))
    ##Door->state

    # a = Point(0, 0)
    # b = Point(3, 0)
    # c = Point(2, 1)
    # d = Point(2, 0)
    remove_duplication()
    # print (total_door)
    G.add_nodes_from(total_door)
    # print(total_door)
    # print (intersect(a, b, c, d))
    # print (intersect(a, c, b, d))
    # print (intersect(a, d, b, c))
    visibility()

    # nx.draw_networkx(G, with_labels=True)
    plt.show()
    canvas.pack()
    btn.pack()
    window.mainloop()

if __name__ == "__main__":
    main()