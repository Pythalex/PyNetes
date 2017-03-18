# -*- coding: utf-8 -*-

# Modules

from sage.calculus.var import *    # var, functions
from sage.functions.trig import *  # cos sin atan2
from sage.functions.other import * # sqrt
from sage.symbolic.ring import SR

# Variables

t         = 0                     # variable de temps
t_inst    = 0                     # Temps immédiat - Calcul des trajectoires temps réel
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
		self.distanceUA = distance_Etoile # en UA
		self.vitesseAng = vitesseAng
		self.nom        = nom
		self.nom_pyimage= -1
		self.masse      = masse

		# Un peu de couleur !
		self.rouge		= 255
		self.vert		= 255
		self.bleu		= 255

		# Propriété coordonnées et mécanique
 		self.equationx       = SR(0)
		self.equationy       = SR(0)
		self.acceleration    = SR(0)
		self.oldacceleration = SR(0)
		self.vitesse         = (SR(0), SR(0))
		self.oldvitesse      = (SR(0), SR(0))
		self.position        = (SR(0), SR(0))
		self.oldposition     = (SR(0), SR(0))
		self.posx            = self.distanceUA * UA
		self.posy            = 0
		self.oldposx         = 0
		self.oldposy         = 0
		self.real_posx       = self.distanceUA * UAKM
		self.real_posy       = 0
		self.oldreal_posx    = 0
		self.oldreal_posy    = 0

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
		global t_inst 

		# Backup des vitesses et positions actuelles pour constantes d'intégrales
		print(type(self.vitesse[0]), type(self.vitesse[1]))
		self.oldvitesse = (fvalue(self.vitesse[0], t_inst), fvalue(self.vitesse[1], t_inst))
		self.oldpostion = (fvalue(self.position[0], t_inst), fvalue(self.position[1], t_inst))
		# Calcul des forces
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
		self.acceleration = (SR(forces / self.masse)*cos(atan2(self.real_posy, self.real_posx)),
			SR(forces / self.masse)*sin(atan2(self.real_posy, self.real_posx)))
		print "Calculating speed vector"
		vecspeed          = (self.acceleration[0].integrate(x), self.acceleration[1].integrate(x))
		self.vitesse      = (vecspeed + self.oldvitesse[0], vecspeed + self.oldvitesse[1])
		print self.vitesse
		vecpos            = (self.vitesse[0].integrate(x)*cos(atan2(self.real_posy, self.real_posx)),
			self.vitesse[1].integrate(x)*sin(atan2(self.real_posy, self.real_posx)))
		print "Calculating position vector"
		self.position     = (vecpos[0] + self.oldreal_posx, vecpos[1] + self.oldreal_posy)
		# reset du temps immédiat
		reset_t_inst()

	def actualiser_position(self):
		global UA
		global UAKM

		self.oldreal_posx = self.real_posx
		self.oldreal_posy = self.real_posy

		self.real_posx = fvalue(self.equationx[0], t_inst)
		self.real_posy = fvalue(self.equationy[1], t_inst)

		self.oldposx = self.posx
		self.oldposy = self.posy

		self.posx = self.real_posx / UAKM * UA
		self.posy = self.real_posy / UAKM * UA

	def get_pos(self):
		return (self.posx, self.posy)

	def get_real_pos(self):
		return (self.real_posx, self.real_posy)


"""
	Global variables changes
"""

def setUA(value):
	global UA
	UA = value

def reset_t_inst():
	t_inst = 0

def time_actualise(TIMESPEED):
	"""
		Actualisation de la variable de temps
	"""

	global t
	global t_inst
	global days
	global timecount
	global years
	global bissextile

	res = 0.0054 * TIMESPEED
	t += res # On compense le temps d'appel de la fonction par un petit ajout au temps
	t_inst += res
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

def distance(planete1, planete2):
	x1, y1 = planete1.get_pos()
	x2, y2 = planete2.get_pos()
	print("planete {}, ({}, {})", planete1, x1, y1)
	print("planete {}, ({}, {})", planete2, x2, y2)

	dist = (sqrt((x2 - x1)**2 + (y2 - y1)**2)).n()
	print("distance in function -> ", dist)
	return dist

def fvalue(function, *args):
	"""
		Retourne la valeur d'une fonction sage avec le 
		nombre d'arguments inférieurs ou égal au nombre
		d'arguments passés par l'utilisateur, si le nombre
		d'arguments est inférieur au nombre de variables
		de la fonction, l'expression littérale est retournée

		EXAMPLE::
		sage: f = 2*x
		sage: fvalue(f, 2, 5)
		4

		---------------------------------------------------

		@param : function la fonction sage à calculer
				 *args la liste des arguments de variables
		@return: f(*args - args en trop)
	"""

	if len(args) == len(function.variables()):
		return function(*args)

	elif len(function.variables()) == 0:
		args = ()

	for variable in function.variables():
		args = args[:-1]
	
	if(len(args) > 0):
		return function(*args)
	else:
		return function()