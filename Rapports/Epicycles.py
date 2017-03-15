"""
	Graphes d'un epicycle

	Soit E, P1, P2 trois points d'un plan tel que :
		
		- E représente une étoile centrale
		- P1 représente une planète 1
		- P2 représente une planète 2

	On souhaite tracer le graphes du mouvement de P1, P2 vu de E,
	puis le mouvement de E, P2 vu de P1

	----

	Python2.7, programmé pour être executé depuis sage

	BONIN Alexandre - Dans le cadre du Projet PyNetes - Math-Info (2017)
"""


# Sage import statements
from sage.plot.plot import plot, parametric_plot
from sage.calculus.var import var
from sage.calculus.var import function
from sage.functions.trig import cos, sin

print("test")

def epicycles():
	
	""" Mouvement vu de E """

	# Données
	t		= var('t') # Variable de temps

	R1		= 75       # Distance entre l'étoile E et P1
	V1		= 1      # Vitesse angulaire de P1 sur l'orbite de E
	teta1_0 = 0        # Angle formé à l'origine avec l'axe des abscisses

	R2		= 100      # Distance entre l'étoile E et P2
	V2      = 0.5      # Vitesse anglaure de P2 sur l'orbite de E
	teta2_0 = pi        # Angle formé à l'origine avec l'axe des abscisses 

	# Vecteurs positions en fonction du temps
	E  = (0, 0)
	P1 = (R1*cos(V1 * t + teta1_0), R1*sin(V1 * t + teta1_0))
	P2 = (R2*cos(V2 * t + teta2_0), R2*sin(V2 * t + teta2_0))

    # Points
	E_pt  = point((0,0))
	P1_pt = point((P1[0](0), P1[1](0)))
	P2_pt = point((P2[0](0), P2[1](0)))

	# Graphe des trajectoires
	graphes = []
	graphes.append(parametric_plot((P1[0], P1[1]), (t, 0, 6*pi)))
	graphes.append(parametric_plot((P2[0], P2[1]), (t, 0, 6*pi)))
	points = [plot(E_pt) + text("E", (6,6)),
              plot(P1_pt) + text("P1", (P1[0](0) + 6, P1[1](0) + 6)),
              plot(P2_pt) + text("P2", (P2[0](0) + 6, P2[1](0) + 6))]
	graphes += points
	plot(sum(graphes)).show()

	""" Mouvement vu de P1 """

	# Vecteurs positions en fonction du temps
	P1 = (0, 0)
	E  = (-R1*cos(V1 * t + teta1_0), -R1*sin(V1 * t + teta1_0))
	P2 = (R2*cos(V2 * t + teta2_0) - R1*cos(V1 * t + teta1_0), 
	   R2*sin(V2 * t + teta2_0) - R1*sin(V1 * t + teta1_0))

	# Points
	E_pt  = point((E[0](0), E[1](0)))
	P1_pt = point((0, 0))
	P2_pt = point((P2[0](0), P2[1](0)))

	# Graphe des trajectoires
	graphes = []
	graphes.append(parametric_plot((E[0], E[1]), (t, 0, 6*pi), color = "#ffaa00"))
	graphes.append(parametric_plot((P2[0], P2[1]), (t, 0, 4*pi), color = "#5555ff"))
	points = [plot(P1_pt) + text("P1", (6,6)),
              plot(E_pt ) + text("E", (E[0](0) + 6, E[1](0) + 6)),
              plot(P2_pt) + text("P2", (P2[0](0) + 6, P2[1](0) + 6))]
	graphes += points
	plot(sum(graphes)).show()

epicycles()