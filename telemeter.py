# -*- coding: utf-8 -*-
"""
Telemetry
"""

from sympy.geometry import Polygon,Line,Point,intersection
from sympy import N
import turtle
import random
from math import *
import numpy as np

import time

def new_box(x,y,c):
    V = turtle.Turtle()
    V.hideturtle(); V.penup()
    V.setpos(x-c/2,y-c/2); V.setheading(0) ; V.pendown()
    for i in range(4):
        V.fd(c)
        V.left(90)
    return Polygon(Point(x-c/2,y-c/2),Point(x-c/2,y+c/2),Point(x+c/2,y+c/2),Point(x+c/2,y-c/2))

def telemetry(T,boxelist):
    a = radians(T.heading())
    P1,P2 = Point(T.xcor(),T.ycor()) , Point(T.xcor()+cos(a),T.ycor()+sin(a))
    P12 = P2 - P1
    intr = [N(P12.dot(p-P1)) for r in boxelist for p in intersection(Line(P1,P2),r) ]
    intr = [d for d in intr if d >= 0]
    #print intr
    return None if intr==[] else (min(intr)+np.random.normal(0,10))

######### main ########
T = turtle.Turtle()
T.tracer(2, 1)
T.penup()

traceur = turtle.Turtle()

boxelist = [ new_box(0,0,600) ]
boxelist = boxelist + [ new_box(150*cos(1+i*2*pi/15),150*sin(1+i*2*pi/15),random.randint(10,40)) for i in range(12)]
boxelist = boxelist + [ new_box(250*cos(1+i*2*pi/25),250*sin(1+i*2*pi/25),random.randint(10,40)) for i in range(20)]

def recupData(nb_mesure):
    data = range(nb_mesure)
    for i in range (nb_mesure):
        data[i] = telemetry(T,boxelist)
        T.left(360/nb_mesure)
        
        traceur.setheading(int(T.heading()))
        traceur.forward(int(data[i]))
        traceur.setpos(0, 0)
    
    return data

def moyenneFlottante(data):
    for i in range(len(data)):
        if i == 0:
            data[0] = (data[-1] + data[0] + data[1]) / 3
        elif i == len(data) - 1:
            data[i] = (data[i] + data[i-1] + data[0]) / 3
        else:
            data[i] = (data[i-1] + data [i] + data[i+1]) / 3

def listeDirections(data):
    choix = []
    cpt = 0
    i = 0

    while i < len(data) * 2 :
        if data[i%len(data)] < 300:
            if cpt >= 8:
                choix.append((float(i%len(data))-cpt/2.0) / len(data) * 360.0)
            cpt = 0
        else:
            cpt += 1
        
        print str(cpt) + " " + str(data[i%len(data)])
            
        i += 1
            
    return choix
    
def choixDirection(data):
    
    direction = 1
    mini = 0
    if len(data) >= 1:
        mini = data[0]
        for value in data:
            if value > 180:
                value = value % 180
                direction = -1
            else:
                direction = 1
            if mini > value:
                mini = value
                
    return mini, direction
        

T.left(90)

data = recupData(60)
moyenneFlottante(data)

"""print data"""
choix = listeDirections(data)

mini, direction = choixDirection(choix)

print "Direction: " + str(direction) + " " + str(mini)

T.left(int(mini) * int(direction))
T.forward(1)
time.sleep(1)
T.forward(150)
time.sleep(1)

raw_input()
