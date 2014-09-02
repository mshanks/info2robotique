#!/usr/bin/python

import math
import turtle
import random

nombre_oiseaux = 20
boids = []
speeds = []
A = 1.0	# influence regle 1
B = 1.0	# influence regle 2
C = 4.0	# influence regle 3
regle1 = []
regle2 = [0, 0]
regle3 = []
regle4 = []
vitesse_const = 1
zone_repulsion = 20
	
# calcul de la distance
def calcul_distance(x1, y1, x2, y2):
	return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

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

turtle.tracer(50, 1)
turtle.hideturtle()
# --
	
while True:
	for i in range(nombre_oiseaux):
		print "%d %s %s" % (i, boids[i].pos(), speeds[i])
		

		
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
				if calcul_distance(boids[i].xcor(), boids[i].ycor(), boid.xcor(), boid.ycor()) < zone_repulsion:
					centre_x += boid.xcor()
					centre_y += boid.ycor()
					nombre += 1
		if nombre > 0:
			centre_x /= nombre
			centre_y /= nombre
		
			regle3[i][0] = -centre_x + boids[i].xcor()
			regle3[i][1] = -centre_y + boids[i].ycor()
	
	
	# on applique les regles
	for i in range(nombre_oiseaux):
		vx, vy = 0, 0
		vx = A * regle1[i][0] + B * regle2[0] + C * regle3[i][0]
		vy = A * regle1[i][1] + B * regle2[1] + C * regle3[i][1]
		boids[i].setheading(math.atan2(vy, vx) * 360 / (2 * math.pi))
		boids[i].forward(vitesse_const)
		
	
	
	
	
	
	
	
	
