import xml.etree.ElementTree as ET
import tkinter
import matplotlib.pyplot as plt
import networkx as nx

from tkinter import *
from PIL import ImageTk, Image


tree = ET.parse('boundary.gml')
root = tree.getroot()
window = tkinter.Tk()
window.title("Indoor Distance")
canvas = tkinter.Canvas(window, width=500, height=500)
img = ImageTk.PhotoImage(Image.open("Door.png"))
total_click = 0

total_line=[]
total_door=[]

G = nx.Graph()
class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def calculate_path():
    print("Caculatepath")

def processOK():
    print("Caculate button is clicked")


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
            total_line.append(input)
        canvas.create_polygon(list, outline='black', fill='ivory3', width=2)

    for i in root.findall("./{http://www.opengis.net/indoorgml/1.0/core}primalSpaceFeatures/{http://www.opengis.net/indoorgml/1.0/core}PrimalSpaceFeatures/{http://www.opengis.net/indoorgml/1.0/core}cellSpaceBoundaryMember/{http://www.opengis.net/indoorgml/1.0/core}CellSpaceBoundary/{http://www.opengis.net/indoorgml/1.0/core}cellSpaceBoundaryGeometry/{http://www.opengis.net/indoorgml/1.0/core}geometry2D/{http://www.opengis.net/gml/3.2}LineString"):
        sum_x=0
        sum_y=0
        for j in i.findall("./{http://www.opengis.net/gml/3.2}pos"):
            words=j.text.split()
            sum_x+=float(words[0])
            sum_y+=float(words[1])
        canvas.create_image(sum_x/2-15, sum_y/2-15, image=img, anchor=NW)
        total_door.append((sum_x/2,sum_y/2))

    a = Point(0, 0)
    b = Point(0, 1)
    c = Point(1, 1)
    d = Point(1, 0)
    G.add_nodes_from(total_door)
    # print (intersect(a, b, c, d))
    # print (intersect(a, c, b, d))
    # print (intersect(a, d, b, c))
    nx.draw_networkx(G, with_labels=True)
    plt.show()
    canvas.pack()
    btn.pack()
    window.mainloop()

if __name__ == "__main__":
    main()