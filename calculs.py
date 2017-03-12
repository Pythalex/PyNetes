# -*- coding: utf-8 -*-

# Modules

from sage.calculus.var import *
from sage.functions.trig import *

# Variables

t = 0                             # variable de temps
timecount = 0
UA        = 200                   # UA <-> px
UAKM      = 149597887.5           # km <-> UA
TIMESPEED = 1                     # Accélération du temps

days      = 0
years     = 0
bissextile= False
x         = var('x')

class Planete(object):

	def __init__(self, nom, taille, distance_Etoile, vitesseAng):
		# Propritété planète
		self.taille     = taille
		self.distanceUA = distance_Etoile               # en UA
		self.distancekm = self.distanceUA * UAKM        # en km
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
			equationx = eval(equationx)
		if(type(equationy) == str):
			equationy = eval(equationy)
		self.equationx = equationx
		self.equationy = equationy

	def get_equation(self):
		return (self.equationx, self.equationy)

	def actualiser_position(self):
		# Si la vérification des types est activée et les équations sont valides
		# Ou si le forcemode est activé
		global UA

		if(self.equationx.has(x)):
			self.posx = UA*self.equationx(t).n()
		else:
			self.posx = UA*self.equationx.n()
		if(self.equationy.has(x)):
			self.posy = UA*self.equationy(t).n()
		else:
			self.posy = UA*self.equationy.n()

	def get_pos(self):
		return (self.posx, self.posy)


"""
	Actualisation du temps
"""
def time_actualise(TIMESPEED):

	global t
	global days
	global timecount
	global years
	global bissextile

	res = 0.0054 * TIMESPEED
	t += res # On compense le temps d'appel de la fonction par un petit ajout au temps
	timecount += res

	print(t, days, years)

	if(int(timecount) / 86400 > 1): # Si une journée est passée
		dayspassed = int(timecount) // 86400
		days += dayspassed
		timecount -= dayspassed * 86400
		if days >= 365 and not bissextile:
			setyears(years + 1)
			days   = 0
			if years % 4 == 0 and not years % 100 == 0 or years % 400 == 0:
				bissextile = True
		elif days >= 366 and bissextile:
			setyears(years + 1)
			days   = 0
			bissextile = False

"""
	Global variables changes
"""

def setUA(value):
	global UA
	UA = value

def setyears(value):
	global years
	years = value
