# -*- coding:utf-8 -*-

from calculs import *

def lire_save(filename):
	file = open(filename, "r")

	liste = []

	next(file) # On saute la ligne des descriptifs
	for line in file:
		line = line.split(";")
		liste.append(line)

	planetes = []

	for elms in liste:
		planete = Planete(elms[0], float(elms[1]), float(elms[2]), float(elms[3]))
		planete.rouge = int(elms[4])
		planete.vert = int(elms[5])
		planete.bleu = int(elms[6])
		planete.set_equation(elms[7], elms[8])
		planetes.append(planete)

	return planetes



if __name__ == "__main__":

	planetes = lire_save("Planetes/planetes.txt")	
	print planetes