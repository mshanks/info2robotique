#!/usr/bin/python
# Parametres ####
N = 10
p = [0., 0.7, 0.2, 0.1]
K = len(p)

def un_char():
	# Cette fonction recupere un caractere aupres de l'utilisateur sans
	# qu'il soit necessaire que celui-ci tape <entree>.
	import sys, tty, termios
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
	  # passage en mode caractere
	  tty.setraw(sys.stdin.fileno())
	  ch = sys.stdin.read(1)
	finally:
	  # retour en mode ligne
	  termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	  return ch

def deplacer_est(t): # une case vers la droite ->
	res = [0 for i in range(N)]
	for i in range(N):
		for j in range(0, min(i + 1, K)):
			res[i] += t[i - j] * p[j]

	for i in range(0, K):
		for j in range(i + 1, K):
			res[N - 1] += t[N - 1 - i] * p[j]
			
	return res

def deplacer_ouest(t): # une case vers la gauche <-
	res = [0 for i in range(N)]
	for i in range(N):
		for j in range(0, min(N - i, K)):
			res[i] += t[i + j] * p[j]
	     	
	for i in range(0, K):
		for j in range(i + 1, K):
			res[0] += t[i] * p[j]
	return res

def main():
	t = [0 for i in range(N)] #terrain (un couloir)
	t[0] = 1. #position initiale
	continuer = True
	while (continuer):
	    affichage_joli = [round(e, 2) for e in t]
	    print affichage_joli # affichage avec moins de decimales
	    c = un_char() # saisie utilisateur
	    if ((c == 'j')  or (c == 'J')):
		t = deplacer_ouest(t)
	    if ((c == 'l')  or (c == 'L')):
		t = deplacer_est(t)
	    if ((c == 'q') or (c == 'Q')):
		continuer = False

main()
