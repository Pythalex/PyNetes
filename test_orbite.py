from Tkinter import *

WIDTH     = 640
HEIGHT    = 480
ORIGIN    = (WIDTH//2, HEIGHT//2) # Origine du repère
t = 0                             # variable de temps
timecount = 0
UA        = 100                    # UA <-> px
TIMESPEED = 3000000               # Accélération du temps

days      = 0
daysPyimage = -1

DAYSTEXTAREA = (WIDTH // 10, HEIGHT // 20)

class Planete(object):

	def __init__(self, taille, distance_Etoile, vitesseAng):
		self.taille     = taille
		self.distanceUA = distance_Etoile * UA          # en UA
		self.distancekm = self.distanceUA * 149597887.5 # en km
		self.vitesseAng = vitesseAng
		self.equationx  = 0
		self.equationy  = 0
		self.posx       = 0
		self.posy       = 0
		self.pyimage    = -1

	def set_equation(self, equationx, equationy):
		self.equationx = equationx
		self.equationy = equationy

	def get_equation(self):
		return (self.equationx, self.equationy)

	def actualiser_position(self, force = False):
		# Si la vérification des types est activée et les équations sont valides
		# Ou si le forcemode est activé
		if(not(force)                                                  and \
		   type(self.equationx) == sage.symbolic.expression.Expression and \
		   type(self.equationy) == sage.symbolic.expression.Expression or  \
		   force):

			self.posx = self.equationx(t).n() + ORIGIN[0]
			self.posy = self.equationy(t).n() + ORIGIN[1]
			

	def get_pos(self):
		return (self.posx, self.posy)


"""
	Methode de Canvas
"""
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle


"""
	Fonction d'animation des planètes

"""
def animation(master, canvas, planete):
	# Actualisation
	canvas.delete(planete.pyimage)
	# time variable
	global t
	# equation horaire
	planete.actualiser_position(force = True)
	# Affichage planète
	planete.pyimage = canvas.create_circle(x = planete.get_pos()[0], 
									       y = planete.get_pos()[1], 
						 				   r = planete.taille,
						 				   fill = "#5555FF")

	# Actualisation canvas
	canvas.update_idletasks()
	# Reanim
	master.after(16, animation, master, canvas, planete)

"""
	Actualisation du temps
"""
def time_actualise(fenetre, canvas):

	global t
	global days
	global timecount

	res = 0.0054 * TIMESPEED
	t += res # On compense le temps d'appel de la fonction par un petit ajout au temps
	timecount += res
	if(int(timecount) % 86400 == 0): # Si une journée est passée
		days += int(timecount) // 86400
		timecount = 0
		daysText(canvas)

	fenetre.after(5, time_actualise, fenetre, canvas)

def daysText(canvas):
	global days
	global daysPyimage

	canvas.delete(daysPyimage)
	daysPyimage = canvas.create_text(DAYSTEXTAREA[0],
									 DAYSTEXTAREA[1],
								     text = "Jours : {}".format(days))


def main():

	fen = Tk()

	can = Canvas(fen, width = WIDTH, height = HEIGHT)
	can.pack()

	can.create_circle(ORIGIN[0], ORIGIN[1], 10, fill = "#FFFF00")

	Terre = Planete(taille = 5, 
					distance_Etoile = 1, 
					vitesseAng = 1.99e-7)
	equationTerre = (Terre.distanceUA * cos(Terre.vitesseAng * x), 
					 Terre.distanceUA * sin(Terre.vitesseAng * x))
	Terre.set_equation(equationTerre[0], equationTerre[1])

	Satellite = Planete(taille = 3,
						distance_Etoile = 0.5,
						vitesseAng = 1.99e-7)
	equationSat = (Satellite.distanceUA * cos(Satellite.vitesseAng * x + pi / 5),
				   Satellite.distanceUA * sin(Satellite.vitesseAng * x + pi / 5))

	Satellite.set_equation(equationSat[0], equationSat[1])

	time_actualise(fen, can)
	animation(fen, can, Terre)
	animation(fen, can, Satellite)
	
	fen.mainloop()

	return 0

main()