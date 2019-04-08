import xml.etree.ElementTree as ET
from tkinter import *
import tkinter

def processOK():
    print("OK button is clicked")

def processCancel():
    print("Cancel button is clicekd")

def click(event):
    print("클릭위치", event.x, event.y)

def main():
    tree = ET.parse('TEST.gml')
    root = tree.getroot()

    window = tkinter.Tk()
    window.title("Indoor Distance")
    canvas = tkinter.Canvas(window)
    canvas.config(width=500,height=500)
    canvas.pack()
    frame = Frame(window, width=500, height=500)
    frame.bind("<Button-1>", click)

    frame.pack()
    for i in root.findall("./{http://www.opengis.net/indoorgml/1.0/core}primalSpaceFeatures/{http://www.opengis.net/indoorgml/1.0/core}PrimalSpaceFeatures/{http://www.opengis.net/indoorgml/1.0/core}cellSpaceMember/{http://www.opengis.net/indoorgml/1.0/core}CellSpace/{http://www.opengis.net/indoorgml/1.0/core}cellSpaceGeometry/{http://www.opengis.net/indoorgml/1.0/core}Geometry2D/{http://www.opengis.net/gml/3.2}Polygon/{http://www.opengis.net/gml/3.2}exterior/{http://www.opengis.net/gml/3.2}LinearRing"):
        list=[]
        for j in i.findall("./{http://www.opengis.net/gml/3.2}pos"):
            words=j.text.split()
            list.append(str(float(words[0])))
            list.append(str(float(words[1])))
        canvas.create_polygon(list, outline='black', fill='ivory3', width=2)
    window.mainloop()

if __name__ == "__main__":
    main()