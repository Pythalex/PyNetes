# -*- coding: utf-8 -*-

# Modules

from sage.calculus.var import *    # var, functions
from sage.functions.trig import *  # cos sin atan2
from sage.functions.other import * # sqrt
from sage.symbolic.ring import SR

# Variables

t = 0                             # variable de temps
timecount = 0
UA        = 200                   # UA <-> px
UAKM      = 149597887.5           # km <-> UA
TIMESPEED = 1                     # Accélération du temps
G         = 6.67e-11              # Constante de gravitation universelle

days      = 0
years     = 0
bissextile= False
x         = var('x')

class Planete(object):

	def __init__(self, nom, taille, distance_Etoile, vitesseAng, masse = 6e24):
		# Propriété planète
		self.taille     = taille
		self.distanceUA = distance_Etoile               # en UA
		self.distancekm = self.distanceUA * UAKM        # en km
		self.vitesseAng = vitesseAng
		self.nom        = nom
		self.nom_pyimage= -1
		self.masse      = masse

		# Un peu de couleur !
		self.rouge		= 255
		self.vert		= 255
		self.bleu		= 255

		# Propriété coordonnées
		self.equationx  = 0
		self.equationy  = 0
		self.posx       = 0
		self.posy       = 0
		self.oldposx    = 0
		self.oldposy    = 0

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

	def actualiser_forces(self, planetes):
		print "Actualize forces"
		forces = []
		for planete in planetes:
			print("planete, ", planete.nom, planete)
			if planete != self:
				# On récupère la distance entre les deux planètes
				pos1  = self.get_pos()
				pos2  = planete.get_pos()
				dist  = distance(pos1, pos2) / UA * UAKM # Distance en km
				print("distance ", dist)
				force = SR(G * planete.masse * self.masse / dist**2)
				forces.append(force)
				print("Gravitational force {} on {} = {}".format(planete.nom, self.nom, force))
		print "sum forces"
		forces = sum(forces)
		print "Calculating acceleration vector"
		self.acceleration = SR(forces / self.masse)
		print "Calculating speed vector"
		self.vitesse      = self.acceleration.integrate(x)
		vecpos            = self.vitesse.integrate(x)
		print "Calculating position vector"
		self.position     = (vecpos + self.oldposx, vecpos + self.oldposy)
		self.set_equation(self.position[0]*cos(atan2(self.get_pos()[1], self.get_pos()[0])), 
			self.position[1]*sin(atan2(self.get_pos()[1], self.get_pos()[0])))

	def actualiser_position(self):
		global UA

		self.oldposx = self.posx
		self.oldposy = self.posy

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
	Global variables changes
"""

def setUA(value):
	global UA
	UA = value

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

	if(int(timecount) / 86400 > 1): # Si une journée est passée
		dayspassed = int(timecount) // 86400
		days += dayspassed
		timecount -= dayspassed * 86400
		if days >= 365 and not bissextile:
			years += 1
			days   = 0
			if years % 4 == 0 and not years % 100 == 0 or years % 400 == 0:
				bissextile = True
		elif days >= 366 and bissextile:
			years += 1
			days   = 0
			bissextile = False

def return_year():
	global years
	return years

def abs(n):
	if n < 0:
		return -n
	return n

def distance(point1, point2):
	print("points, ", point1, point2)
	dist = (sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)).n()
	print("distance in function -> ", dist)
	return dist