# -*- coding: utf-8 -*-

from calculs import *

def lire_fichier(filename):

	file = open(filename, "r")

	liste = []

	for line in file:
		line = line.split(";")
		liste.append(line)

	return liste

def lire_save(filename):

	liste = lire_fichier(filename)
	liste.remove(liste[0]) # Descriptions planetes

	planetes = []

	for elms in liste:
		planete = Planete(elms[0], float(elms[1]), float(elms[2]), float(elms[3]))
		planete.rouge = int(elms[4])
		planete.vert = int(elms[5])
		planete.bleu = int(elms[6])
		planetes.append(planete)

	return planetes

def save_planete(filename, planete):

		liste = lire_fichier(filename)
		liste.reverse()
		count = 0
		elm   = liste[count]
		while elm in ['\n', '\r\n', '\r', ' ']:
			liste.remove(elm)
			count += 1
			elm    = liste[count]

		liste.reverse()
		liste.append([planete.nom, planete.taille, planete.distanceUA, planete.vitesseAng, planete.rouge, planete.vert, planete.bleu, "self.distanceUA*cos(self.vitesseAng*t)", "self.distanceUA*sin(self.vitesseAng*t)", "\r\n"])

		ecrire = open(filename, "w+")

		for planete in liste:
			for elm in planete:
				ecrire.write(str(elm))
				if elm != '\r\n' and elm != '\n' :
					ecrire.write(";")

		ecrire.close() # On ferme le fichier, sinon on ne peut pas importer directement la planète sauvegardée !


if __name__ == "__main__":

	planetes = lire_save("Planetes/planetes.pyns")	
	print planetes
