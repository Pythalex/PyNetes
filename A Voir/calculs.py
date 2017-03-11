# -*- coding: utf-8 -*-

# Modules

from sage.all import *

# Variables

t = 0                             # variable de temps
timecount = 0
UA        = 100                    # UA <-> px
TIMESPEED = 1                     # Accélération du temps
NBPLANETE = 0

days      = 0
x         = var('x')

class Planete(object):

	def __init__(self, nom, taille, distance_Etoile, vitesseAng):
		# Propritété planète
		self.taille     = taille
		self.distanceUA = distance_Etoile * UA          # en UA
		self.distancekm = self.distanceUA * 149597887.5 # en km
		self.vitesseAng = vitesseAng
		self.nom        = nom
		self.nom_pyimage= -1

		# Un peu de couleur !
		self.rouge		= 255
		self.vert		= 255
		self.bleu		= 255

		# Propriété coordonnées
		self.equationx  = 0
		self.equationy  = 0
		self.posx       = 0
		self.posy       = 0

		# Propriété Tkinter
		self.pyimage    = -1
		self.delete     = False

	def set_equation(self, equationx, equationy):
		if(type(equationx) == str):
			equationx = sage_eval(equationx, locals={'distanceUA': self.distanceUA, 'vitesseAng': self.vitesseAng, 't' : x})
		if(type(equationy) == str):
			equationy = sage_eval(equationy, locals={'distanceUA': self.distanceUA, 'vitesseAng': self.vitesseAng, 't' : x})
		self.equationx = equationx
		self.equationy = equationy

	def get_equation(self):
		return (self.equationx, self.equationy)

	def actualiser_position(self, ORIGIN):
		# Si la vérification des types est activée et les équations sont valides
		# Ou si le forcemode est activé

		if(self.equationx.has(x)):
			self.posx = self.equationx(t).n() + ORIGIN[0]
		else:
			self.posx = self.equationx.n() + ORIGIN[0]
		if(self.equationy.has(x)):
			self.posy = self.equationy(t).n() + ORIGIN[1]
		else:
			self.posy = self.equationy.n() + ORIGIN[1]

	def get_pos(self):
		return (self.posx, self.posy)


"""
	Actualisation du temps
"""
def time_actualise(TIMESPEED):

	global t
	global days
	global timecount

	res = 0.0054 * TIMESPEED
	t += res # On compense le temps d'appel de la fonction par un petit ajout au temps
	timecount += res

	if(int(timecount) % 86400 == 0): # Si une journée est passée
		days += int(timecount) // 86400
		timecount = 0