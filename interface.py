# -*- coding: utf-8 -*-
from Tkinter    import *
from calculs    import *
from file       import *

class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

def _draw_planet(planete):
	x, y = planete.get_pos()
	r    = planete.taille
	color= planete.couleur
	return self.create_oval(x-r, y-r, x+r, y+r, fill = couleur)
Canvas.draw_planet = _draw_planet

class Application(Tk):

	# Initialisations
	def initApp(self):
		# Frames canvas et liste des planètes
		self.frame1 = Frame()
		self.frame2 = Frame()
		

		self.canvas = Canvas(self.frame1, 
						     width  = 640, 
						     height = 480,
						     bg     = "#000000") # black background

		# Variables
		self.terre_select    = IntVar()
		self.satelite_select = IntVar()
		self.custom_taille   = StringVar()
		self.custom_distance = StringVar()
		self.custom_vitesse  = StringVar()
		self.custom_nom      = StringVar()

		# Frame de sélection des planètes pour affichage
		self.select_planets  = LabelFrame(self.frame2, text="Planètes")

		self.select_planets1 = Checkbutton(self.select_planets, text = "Terre",    variable = self.terre_select)
		self.select_planets2 = Checkbutton(self.select_planets, text = "Satelite", variable = self.satelite_select)
		self.bouton_actu     = Button(self.select_planets,      text = "Actualiser", 
													            command = lambda : SelectPlanete(self.terre_select, 
													  	                             self.satelite_select))

		# Frame de création des planètes
		self.create_planets        = LabelFrame(self.frame2,     text = "Création")
		self.label_create_taille   = Label(self.create_planets,  text = "Taille")
		self.create_taille         = Entry(self.create_planets,  textvariable = self.custom_taille)
		self.label_create_distance = Label(self.create_planets,  text = "Distance")
		self.create_distance       = Entry(self.create_planets,  textvariable = self.custom_distance)
		self.label_create_vitesse  = Label(self.create_planets,  text = "Vitesse")
		self.create_vitesse        = Entry(self.create_planets,  textvariable = self.custom_vitesse)
		self.label_create_nom      = Label(self.create_planets,  text = "Nom")
		self.create_nom            = Entry(self.create_planets,  textvariable = self.custom_nom)
		self.bouton_create         = Button(self.create_planets, text = "Créer", 
															     command = lambda : AutrePlanete(self.custom_taille, 
																						  self.custom_distance, 
																						  self.custom_vitesse))

		# Placements widgets
		self.frame1.grid(row = 0, column = 0)

		self.canvas.grid(row = 0, column = 0)

		self.frame2.grid(row = 0, column = 1)

		self.select_planets.grid(row = 0, column = 0)
		self.select_planets1.grid(row = 0, column = 0, sticky = W)
		self.select_planets2.grid(row = 1, column = 0, sticky = W)
		self.bouton_actu.grid(row = 2, column = 0)

		self.create_planets.grid(row = 1, column = 0)
		self.label_create_taille.grid(row = 0, column = 0, sticky = W)
		self.create_taille.grid(row = 0, column = 1)
		self.label_create_distance.grid(row = 1, column = 0, sticky = W)
		self.create_distance.grid(row = 1, column = 1)
		self.label_create_vitesse.grid(row = 2, column = 0, sticky = W)
		self.create_vitesse.grid(row = 2, column = 1)
		self.label_create_nom.grid(row = 3, column = 0, sticky = W)
		self.create_nom.grid(row = 3, column = 1)
		self.bouton_create.grid(row = 4, column = 0, columnspan = 2)

		# binds
		self.bouton_create.config(command = self.ajouter_planete)

		# Variables de simulation
		self.planetes = []

	# Methodes
	def time(self):
		# Incrémenter compteur temps
		time_actualise()
		# Recommencez après 5 ms
		self.after(5, self.time)

	def animation(self):
		compteur = 0
		while compteur < len(self.planetes):
			planete = self.planetes[compteur]

			# Si la planete a été marquée 
			if(planete.delete):
				del self.planetes[compteur]
				break

			self.canvas.delete(planete.pyimage)

			print "\n\nDEBUG animation line 125\n\n"
			print planete.equationx.has(x)
			print "\n\nDEBUG FIN\n\n"
			planete.actualiser_position(force = True)

			self.canvas.draw_planet(planete)

		self.after(16, self.animation)

	def ajouter_planete(self):

		# On crée la planète correspondante aux données du GUI
		planete = Planete(self.custom_nom.get(), 
						  float(self.custom_taille.get()), 
						  float(self.custom_distance.get()), 
						  float(self.custom_vitesse.get()))
		equation = (planete.distancekm * cos(planete.vitesseAng * x),
					planete.distancekm * sin(planete.vitesseAng * x))
		planete.set_equation(equation[0], equation[1])

		# On l'ajoute à la liste des planetes
		self.planetes.append(planete)

	def update(self):
		self.time()
		self.animation()

def main():

	process = Application()
	process.initApp()

	process.update()

	process.mainloop()

	return 0

main()