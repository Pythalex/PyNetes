# -*- coding: utf-8 -*-
from Tkinter    import *
from calculs    import *
from file       import *
from sage import *

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

def _draw_planet(self, planete):
	x, y = planete.get_pos()
	r    = planete.taille
	color= planete.couleur
	return self.create_oval(x-r, y-r, x+r, y+r, fill = color)
Canvas.draw_planet = _draw_planet

class Planete_Prop_Window(Tk):

	def __init__(self, planete):
		Tk.__init__(self)
		self.planete = planete
		self.planete_name = Label(text = planete.nom)
		self.planete_pos  = Label(text = "Position : {}".format((planete.get_pos())))

class Planete_Bouton(Button):

	def __init__(self, planete, master, **kwargs):
		Button.__init__(self, master, kwargs)
		self.est_affiche = False
		self.planete     = planete

	def afficher_fenetre(self):
		Planet_Prop_Window(planete)

class Error_Window(Tk):

	def __init__(self, message):
		Tk.__init__(self)
		self.title("PyNetes ERROR")
		self.geometry("200x100")
		Label(master = self, text = message).pack(anchor = CENTER)

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
		self.select_planets_frame  = LabelFrame(self.frame2, text="Planètes")
		self.planete_var = globals()
		self.boutons_planetes = []
		self.selected_planets = []
		self.planetes_noms    = []

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
															     command = self.ajouter_planete)

		# Placements widgets
		self.frame1.grid(row = 0, column = 0)

		self.canvas.grid(row = 0, column = 0)

		self.frame2.grid(row = 0, column = 1)

		self.select_planets_frame.grid(row = 0, column = 0)

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

		# Variables de simulation
		self.planetes = []

	def select_planets(self, planetes):
		for planete in planetes:
			self.ajouter_planete(planete)

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

			planete.actualiser_position(force = True)

			planete.pyimage = self.canvas.draw_planet(planete)

			compteur += 1

		self.canvas.update_idletasks()
		self.after(16, self.animation)

	def ajouter_planete(self):
		# On crée la planète correspondante aux données du GUI
		planete = Planete(self.custom_nom.get(), 
						  float(self.custom_taille.get()), 
						  float(self.custom_distance.get()), 
						  float(self.custom_vitesse.get()))
		equation = (planete.distanceUA * cos(planete.vitesseAng * x),
					planete.distanceUA * sin(planete.vitesseAng * x))
		planete.set_equation(equation[0], equation[1])

		# On l'ajoute à la liste des planetes
		self.planetes.append(planete)
		# On crée le bouton associé à la planète
		self.ajouter_bouton_planete(planete)

	def ajouter_bouton_planete(self, planete):
			
		# Si le nom de la planète est déjà pris
		if planete.nom in self.planetes_noms:
			# On affiche une erreur
			Error_Window(message = "{} existe déjà.".format(planete.nom))

		else:
			self.planete_var[planete.nom] = planete
			self.planetes_noms.append(planete.nom)

		# Sinon ça marche
		"""
		except NameError:
			self.planete_var[planete.nom] = planete
			self.boutons_planetes.append(self.planete_var[planete.nom])
			self.boutons_planetes.append(Planete_Bouton())
			"""
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