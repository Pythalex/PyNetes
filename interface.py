# -*- coding: utf-8 -*-
from Tkinter    import *
from calculs    import *
from file       import *
from sage import *

sCENTER = W + E

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

	def __init__(self, planete, bouton):
		Tk.__init__(self)
		self.planete = planete

		self.planete_name  = Label(master = self, text = planete.nom)

		self.posx = StringVar()
		self.posx.set("Position x : {0:0.1f}".format(float(planete.get_pos()[0])))
		self.posy = StringVar()
		self.posy.set("Position y : {0:0.1f}".format(float(planete.get_pos()[1])))

		self.planete_pos_x = Label(master = self, textvariable = self.posx)
		self.planete_pos_y = Label(master = self, textvariable = self.posy)

		self.bouton_switch = Button(self, text = "Afficher", command = bouton.switch)

		self.planete_name.grid(row = 0, column = 0, 
			rowspan = 2, columnspan = 2)
		self.planete_pos_x.grid(row = 2, column = 0)
		self.planete_pos_y.grid(row = 3, column = 0)
		self.bouton_switch.grid(row = 4, column = 0)

class Planete_Bouton(Button):

	def __init__(self, planete, master, boutons, **kwargs):
		Button.__init__(self, master, kwargs)
		# Si la planete est actuellement affiché
		self.est_affiche = True
		# Si la planete doit être affiché 
		self.affiche     = True
		# Si le bouton doit être supprimé
		self.to_delete   = False

		self.grid(row = len(boutons), column = 0)

		self.configure(text = self.planete.nom,
			command = self.afficher_fenetre)

	""" Affiche la fenêtre des propriétés de la planète """
	def afficher_fenetre(self):
		Planete_Prop_Window(self.planete, self)

	""" Cache la planete sans l'effacer """
	def hide(self):
		if self.est_affiche:
			self.affiche = False

	""" Affiche la planete """
	def show(self):
		self.boutons = boutons
		if not self.est_affiche:
			self.affiche = True

	""" Supprime la planete et le bouton """
	def delete(self):
		self.to_delete = True
		self.affiche   = False

	""" Change le bouton en on/off """
	def switch(self):
		if self.est_affiche:
			self.hide()
		else:
			self.show(self.boutons)


class Error_Window(Tk):

	def __init__(self, message):
		Tk.__init__(self)
		self.title("PyNetes ERROR")
		self.canvas = Canvas(master = self, width = 100, height = 100)
		self.canvas.pack()
		self.resizable(width=False, height=False)
		self.message = Label(master = self.canvas, text = message)
		self.message.grid(row = 0, column = 0, padx = 10, pady = 10)

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
		self.planetes = []
		self.boutons_planetes = []
		self.selected_planetes = []
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
		while compteur < len(self.selected_planetes):
			planete = self.selected_planetes[compteur]

			self.canvas.delete(planete.pyimage)

			planete.actualiser_position(force = True)

			planete.pyimage = self.canvas.draw_planet(planete)

			compteur += 1

		self.canvas.update_idletasks()
		self.after(16, self.animation)

	def ajouter_planete(self):

		# Si le nom de la planète est déjà pris
		if self.custom_nom.get() in self.planetes_noms:
			# On affiche une erreur
			Error_Window(message = "{} existe déjà.".format(self.custom_nom.get()))
			return 1

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
		self.selected_planetes.append(planete)
		# On crée le bouton associé à la planète
		self.ajouter_bouton_planete(planete)

	def ajouter_bouton_planete(self, planete):

		# On ajoute la planète a la liste des planètes de l'utilisateur
		self.planetes.append(planete)
		self.planetes_noms.append(planete.nom)
		# On ajoute un nouveau bouton à la fenêtre
		self.boutons_planetes.append(Planete_Bouton(planete, self.select_planets_frame))
		# On affiche le bouton
		self.boutons_planetes[-1].show(self.boutons_planetes)

	def refresh_planetes(self):
		for bouton in self.boutons_planetes:
			# Si la planète est à cacher
			if not bouton.affiche and bouton.est_affiche:
				self.selected_planetes.remove(bouton.planete)
				bouton.est_affiche = False
				bouton.grid_forget()
			# Si la planete est à réafficher
			elif bouton.affiche and not bouton.est_affiche:
				self.selected_planetes.append(bouton.planete)
				bouton.est_affiche = True
				bouton.grid(row = len(self.boutons_planetes), column = 0)
			# Si la planète est à supprimer
			elif bouton.to_delete:
				self.selected_planetes.remove(bouton.planete)
				self.planetes.remove(bouton.planete)
				boutons_planetes.remove(bouton)
				bouton.destroy()

		self.after(16, self.refresh_planetes)

	def update(self):
		self.time()
		self.animation()
		self.refresh_planetes()

def main():

	process = Application()
	process.initApp()

	process.update()

	process.mainloop()

	return 0

main()