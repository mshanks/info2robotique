# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 10:19:02 2014

@author: personne
"""

import nxt, thread, time

b = nxt.find_one_brick()
mTourelle = nxt.Motor(b, nxt.PORT_A)

sonar = nxt.sensor.Ultrasonic(b,nxt.PORT_1)


def mesure(nb_mesure):
    data = range(nb_mesure - 1)
    mTourelle.reset_position(True)
    mTourelle.reset_position(False)
    str1, var1= mTourelle.get_tacho()
    print var1
    mTourelle.weak_turn(100, int(360/nb_mesure))
    """
    while mTourelle.get_tacho() < 360 :
        mTourelle.turn(100, int(360/nb_mesure), brake=True, timeout=1, emulate=True)
        data[0] = sonar.get_sample()
        print mTourelle.get_tacho()
    """
    return data

# pour terminer le programme proprement
def terminer():
    mTourelle.run(0)
    exit(0)

try:
    data = mesure(36)
    for i in range(len(data)) :
        print str(i) + " " + str(data[i])
    
    terminer()
except KeyboardInterrupt:
    terminer()