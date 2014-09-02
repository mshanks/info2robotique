#!/usr/bin/python

import math
import turtle
import random

nombre_oiseaux = 15
boids = []
speeds = []
A = 1.0	# influence regle 1
B = 50.0	# influence regle 2
C = 4.0	# influence regle 3
D = 1000.0# influence regle 4 - empeche de sortir de la fenetre
E = 1   # influence regle 5 - prend en compte la vitesse precedente
regle1 = []
regle2 = [0, 0]
regle3 = []
regle4 = []
regle5 = []
vitesse_const = 1
zone_repulsion = 20

# init boids
for i in range(nombre_oiseaux):
	boid = turtle.Turtle()
	boid.speed("fastest")
	# parametre aleatoire
	boid.penup()
	boid.setpos(random.randint(-200, 200), random.randint(-200, 200))
	boid.setheading(random.randint(0, 359))
	#boid.pendown()
	boid.color(random.random(), random.random(), random.random())
	
	speed = [random.randint(10, 20), random.randint(10, 20)]
	
	# ajout du boid
	boids.append(boid);
	speeds.append(speed)
	
	regle1.append([0, 0])
	regle3.append([0, 0])
	regle4.append([0, 0])
	regle5.append([0, 0])

turtle.tracer(50, 1)
turtle.hideturtle()
# --
	
while True:
	hauteur, largeur = turtle.screensize()
		
	# calcul de la position moyenne -- regle 1
	for i in range(nombre_oiseaux):
		centre_x, centre_y = 0, 0	
		for boid in boids:
			centre_x += boid.xcor()
			centre_y += boid.ycor()
		centre_x /= nombre_oiseaux
		centre_y /= nombre_oiseaux
		
		regle1[i][0] = centre_x - boids[i].xcor()
		regle1[i][1] = centre_y - boids[i].ycor()


	# calcul de la vitesse moyenne -- regle 2
	angle = 0
	for boid in boids:
		angle += boid.heading()
	angle /= nombre_oiseaux
	angle *= (2 * math.pi) / 360
	regle2[0] = math.cos(angle)
	regle2[1] = math.sin(angle)
			

	# calcul de la zone de repulsion -- regle 3
	for i in range(nombre_oiseaux):
		centre_x, centre_y = 0, 0
		nombre = 0
		for boid in boids:
			if boid != boids[i]:
				if boids[i].distance(boid) < zone_repulsion:
					centre_x += boid.xcor()
					centre_y += boid.ycor()
					nombre += 1
		if nombre > 0:
			centre_x /= nombre
			centre_y /= nombre
		
			regle3[i][0] = -centre_x + boids[i].xcor()
			regle3[i][1] = -centre_y + boids[i].ycor()
		
			
	# calcul de la taille de la fenetre -- regle 4
	for i in range(nombre_oiseaux):
		regle4[i][0] = 0
		regle4[i][1] = 0
		if boids[i].xcor() > largeur:
			regle4[i][0] = -10
		elif boids[i].xcor() < - largeur:
			regle4[i][0] = 10
			
		if boids[i].ycor() > hauteur:
			regle4[i][1] = -10
		elif boids[i].ycor() < - hauteur:
			regle4[i][1] = 10
	
	# calcul de la vitesse precedente -- regle 5
	for i in range(nombre_oiseaux):
		regle5[i][0] = speeds[i][0]
		regle5[i][1] = speeds[i][1]
		
		
	# on applique les regles
	for i in range(nombre_oiseaux):
		speeds[i][0] = A * regle1[i][0] + B * regle2[0] + C * regle3[i][0] + D * regle4[i][0] + E * regle5[i][0]
		speeds[i][1] = A * regle1[i][1] + B * regle2[1] + C * regle3[i][1] + D * regle4[i][1] + E * regle5[i][1]
		boids[i].setheading(math.atan2(speeds[i][1], speeds[i][0]) * 360 / (2 * math.pi))
		boids[i].forward(vitesse_const)
		
	
	
	
	
	
	
	
	
