# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 10:19:02 2014

@author: personne
"""

import nxt, thread, time
import turtle

t = None
b = nxt.find_one_brick()
mTourelle = nxt.Motor(b, nxt.PORT_A)
mGauche = nxt.Motor(b, nxt.PORT_B)
mDroite = nxt.Motor(b, nxt.PORT_C)

sonar = nxt.sensor.Ultrasonic(b,nxt.PORT_1)

# fonction pour avancer - prend en parametre la puissance a applique sur les roues
def avancer(puissance):
    mGauche.run(puissance)
    mDroite.run(puissance)


# fonction pour stoper le moteur gauche
def stop_gauche():
    mGauche.brake()

# fonction pour stocker le moteur droit
def stop_droite():
    mDroite.brake()

# fonction pour stoper les deux moteurs
def stop():
    stop_droite()
    stop_gauche()

# fonction pour tourner a droite
def tournerDroite(angle):
    thread.start_new_thread(mGauche.turn,(100,angle))
    mDroite.turn(-100,angle)
    time.sleep(0.1)
    
def tournerGauche(angle):
    thread.start_new_thread(mDroite.turn,(100,angle))
    mGauche.turn(-100,angle)
    time.sleep(0.1)
    

def mesure(nb_mesure):
    # Nombres de mesures dans le tableau
    data1 = range(nb_mesure)
    angle1 = range(nb_mesure)
    data2 = range(nb_mesure)
    angle2 = range(nb_mesure)
    for i in range(nb_mesure):
        data1[i] = -1
        data2[i] = -1
        angle1[i] = -1
        angle2[i] = -1
    # Reset des tacho de la tourelle
    mTourelle.reset_position(False)
    mTourelle.reset_position(True)
    # Mesure angulaire
    delta = 360*9
    
    i = 0
    
    while mTourelle.get_tacho().block_tacho_count < delta and i < nb_mesure :
        data1[i] = sonar.get_sample()
        angle1[i] = mTourelle.get_tacho().block_tacho_count / 9
        #Amelioration du nombre de mesure        
        #time.sleep(1)
        mTourelle.turn(100, int(delta/nb_mesure), brake=True, timeout=1, emulate=True)
        mTourelle.brake()
        i += 1
    i = 0
    mTourelle.brake()
    time.sleep(0.5)
    while mTourelle.get_tacho().block_tacho_count > 0 and i < nb_mesure :
        data2[nb_mesure - 1 - i] = sonar.get_sample()
        angle2[i] = mTourelle.get_tacho().block_tacho_count / 9
        #Amelioration du nombre de mesure        
        #time.sleep(1)
        mTourelle.turn(-100, int(delta/nb_mesure), brake=True, timeout=1, emulate=True)
        mTourelle.brake()
        i += 1
    
    return data1, angle1, data2, angle2
    
def moyenne(nb_mesure, data1, data2):
    data = range(nb_mesure)
    for i in range(nb_mesure):
        if data1[i] > -1 and data2[i] > -1:
            data[i] = (data1[i] + data2[i]) / 2
        elif data[i] == -1 and data2[i] > -1:
            data[i] = data2[i]
        elif data[i] > -1 and data2[i] == -1:
            data[i] = data1[i]
    
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
        if data[i%len(data)] < 50:
            """ Le robot passe au minimum dans un angle de 8 """
            if cpt >= 5:
                choix.append((float(i%len(data))-cpt/2.0) / len(data) * 360.0)
            cpt = 0
        else:
            cpt += 1
            
        i += 1
            
    return choix

def choixDirection(data):
    directionMini = 180
    
    for i in range(len(data)):
        if data[i] > 180:
            data[i] = -180 + (data[i] % 180)
    
    for j in range(len(data)):
        if directionMini > abs(data[j]):
            directionMini = data[j]
    
    return directionMini
    
def dessiner(data, angle):
    
    for i in range(len(data)):
        turtle.setheading(int(angle[i]))
        turtle.forward(int(data[i]))
        turtle.setpos(0, 0)
            

def analyse_environement():
    data1, angle1, data2, angle2 = mesure(36)
    
    data = moyenne(36, data1, data2)
    
    moyenneFlottante(data)
    
    print data
    
    turtle.clearscreen()
    dessiner(data, angle1)
    
    choix = listeDirections(data)
    direction = choixDirection(choix)
    
    return direction
    
    
# pour terminer le programme proprement
def terminer():
    mTourelle.brake()
    time.sleep(0.5)
    mTourelle.run(0)
    avancer(0)
    exit(0)

try:
    while True:
        direction = analyse_environement()
        print direction
        if direction > 0:
            tournerDroite(direction * 5)
        else:
            tournerGauche(-direction * 5)
            
        avancer(100)
        while sonar.get_sample() > 40:
            time.sleep(0.2)
        stop()
        
    stop()
    
    terminer()
except KeyboardInterrupt:
    terminer()