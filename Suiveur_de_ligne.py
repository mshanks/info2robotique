#####################################
# TP Robotique - Suiveur de ligne   #
# Par Julien Raison et Thomas Guiot #
#####################################

# Pour changer de direction, il suffit d'inverser les ports des moteurs

import nxt, thread, time

b = nxt.find_one_brick()
mGauche = nxt.Motor(b, nxt.PORT_C)
mDroite = nxt.Motor(b, nxt.PORT_B)

lux = nxt.sensor.Color20(b, nxt.PORT_3)

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
def tournerDroite():
    mGauche.weak_turn(80, 10)
    mDroite.weak_turn(-60, 10)

# pour terminer le programme proprement
def terminer():
    avancer(0)
    lux.get_reflected_light(nxt.sensor.Type.COLORNONE)
    exit(0)

# Boucle principale
try:
    while True:
        
        # On recupere la luminosite sous le capteur
        luminosite = lux.get_reflected_light(nxt.sensor.Type.COLORGREEN)
        
        if luminosite < 200:    # Si < a 200 (on est sur la ligne)
            avancer(70)         # On avance
        
        else:   # sinon, on tourne a droite apres avoir bloquer les roues
            stop()
            tournerDroite()
            
    terminer()
    
except KeyboardInterrupt:
    terminer()