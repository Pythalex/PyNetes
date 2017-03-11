# -*- coding: utf-8 -*-
from Tkinter    import *
from calculs    import *
from file       import *
from sage import *

sCENTER = W + E

class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind 		("<Configure>", self.on_resize)
        self.height  	= self.winfo_reqheight()
        self.width  	= self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale  		= float(event.width)/self.width
        hscale  	 	= float(event.height)/self.height
        self.width  	= event.width
        self.height 	= event.height
        # resize the canvas 
        self.config 	(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale 		("all",0,0,wscale,hscale)

# Du décimal vers de l'héxa.
def conv(chiffre):
		def chiftolet(chiffre):
			convertion = ["a", "b", "c", "d", "e", "f"]
			if chiffre >= 10:
				chiffre -= 10
				return convertion[chiffre]
			return chiffre
		reste = 20
		actu  = chiffre
		liste = []
		fin   = ""
		while reste >= 16:
			reste = actu % 16
			actu  = actu / 16
			liste.append(reste)
		fin += str(chiftolet(actu))
		for elems in liste:
			fin += str(chiftolet(elems))
		return fin

def _draw_planet(self, planete):
	x, y = planete.get_pos()
	r    = planete.taille/2
	color = "#" + conv(planete.rouge) + conv(planete.vert) + conv(planete.bleu)
	return self.create_oval(x-r, y-r, x+r, y+r, fill = color)
Canvas.draw_planet = _draw_planet

class Planete_Prop_Window(Toplevel):

	def __init__(self, master, planete, bouton):
		Toplevel.__init__(self)
		self.master  					= master
		self.planete 					= planete
		self.planete_name  				= Label(master = self, text = planete.nom)

		# Affichage
		self.posx 						= StringVar()
		self.posx.set					("Position x : {0:0.1f}".format(float(planete.get_pos()[0])))
		self.posy 						= StringVar()
		self.posy.set					("Position y : {0:0.1f}".format(float(planete.get_pos()[1])))


		self.planete_taille 			= IntVar()
		self.planete_taille.set 		(self.planete.taille)

		self.boutonrouge 				= IntVar()
		self.boutonrouge.set 			(self.planete.rouge)

		self.boutonvert 				= IntVar()
		self.boutonvert.set 			(self.planete.vert)

		self.boutonbleu 				= IntVar()
		self.boutonbleu.set 			(self.planete.bleu)


		self.planete_pos_x 				= Label(master = self, textvariable = self.posx)
		self.planete_pos_y 				= Label(master = self, textvariable = self.posy)


		self.planete_taille_label		= Label(master = self, text = "Taille")
		self.planete_taille_value		= Spinbox(master = self, from_ = 0, to    = 1000, textvariable = self.planete_taille)


		self.label_spin_rouge 			= Label(self, text = "Rouge")
		self.spin_rouge 				= Spinbox(self, from_ = 0, to = 255, textvariable = self.boutonrouge)

		self.label_spin_vert 			= Label(self, text = "Vert")
		self.spin_vert  				= Spinbox(self, from_ = 0, to = 255, textvariable = self.boutonvert)

		self.label_spin_bleu 			= Label(self, text = "Bleu")
		self.spin_bleu  				= Spinbox(self, from_ = 0, to = 255, textvariable = self.boutonbleu)


		self.bouton_switch 				= Button(self, text = "Afficher / Masquer", command = bouton.switch)


		self.planete_name.grid 			(row = 0, column = 0, rowspan = 2, columnspan = 2)

		self.planete_pos_x.grid 		(row = 2, column = 0, columnspan = 2)
		self.planete_pos_y.grid 		(row = 3, column = 0, columnspan = 2)

		self.bouton_switch.grid 		(row = 4, column = 0, columnspan = 2)

		self.planete_taille_label.grid	(row = 5, column = 0)
		self.planete_taille_value.grid	(row = 5, column = 1)

		self.label_spin_rouge.grid		(row = 6, column = 0)
		self.spin_rouge.grid			(row = 6, column = 1)

		self.label_spin_vert.grid		(row = 7, column = 0)
		self.spin_vert.grid				(row = 7, column = 1)

		self.label_spin_bleu.grid		(row = 8, column = 0)
		self.spin_bleu.grid				(row = 8, column = 1)

		self.refresh()

	def refresh(self):
		self.planete.rouge 				= self.boutonrouge.get()
		self.planete.vert 				= self.boutonvert.get()
		self.planete.bleu 				= self.boutonbleu.get()
		self.posx.set 					("Position x : {0:0.1f}".format(float(self.planete.get_pos()[0])))
		self.posy.set 					("Position y : {0:0.1f}".format(float(self.planete.get_pos()[1])))

		self.planete.taille 			= self.planete_taille.get()

		self.after 						(30, self.refresh)

class Planete_Bouton(Button):

	def __init__(self, master, planete, length):
		Button.__init__(self, master = master)

		# Si la planete est actuellement affiché
		self.est_affiche 	= True

		# Si la planete doit être affiché 
		self.affiche 		= True

		# Si le bouton doit être supprimé
		self.to_delete 		= False

		# La planète associée au bouton
		self.planete 		= planete

		# Frame boutons
		self.master			= master

		self.grid			(row = length, column = 0)

		self.configure 		(text = self.planete.nom, command = self.afficher_fenetre)


	""" Affiche la fenêtre des propriétés de la planète """
	def afficher_fenetre(self):
		Planete_Prop_Window(self.master, self.planete, self)

	""" Cache la planete sans l'effacer """
	def hide(self):
		if self.est_affiche:
			self.affiche = False

	""" Affiche la planete """
	def show(self):
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
			self.show()


class Error_Window(Toplevel):

	def __init__(self, master, message):
		Toplevel.__init__ 	(self)

		self.title 			("PyNetes ERROR")
		self.canvas 		= Canvas(master = self, width = 100, height = 100)
		self.canvas.pack	()
		self.resizable 		(width=False, height=False)
		self.message  		= Label(master = self.canvas, text = message)
		self.message.grid 	(row = 0, column = 0, padx = 10, pady = 10)


class Application(Tk):

	# Initialisations
	def initApp(self):
		# Frames canvas et liste des planètes
		self.frame1 						= Frame()
		self.frame2 						= Frame()
		

		self.canvas 						= Canvas(self.frame1, width = 640, height = 480, bg = "#000000") # black background

		# Variables
		self.terre_select 					= IntVar()
		self.satelite_select 				= IntVar()
		self.custom_taille 					= StringVar()
		self.custom_distance 				= StringVar()
		self.custom_vitesse 				= StringVar()
		self.custom_nom 					= StringVar()
		self.time_reglage 					= IntVar()

		# Frame des reglages
		self.reglages_frame 				= LabelFrame(self.frame2, text = "Configurations")
		self.label_time_spinbox 			= Label(self.reglages_frame,  text = "Vitesse")
		self.time_spinbox   				= Spinbox(self.reglages_frame, from_ = -100, to = 100, textvariable = self.time_reglage)
		self.time_reglage.set 				(1)

		# Frame de sélection des planètes pour affichage
		self.select_planets_frame 			= LabelFrame(self.frame2, text="Planètes")
		self.planetes 						= []
		self.boutons_planetes 				= []
		self.selected_planetes 				= []
		self.planetes_noms    				= []

		# Frame de création des planètes
		self.create_planets_frame 			= LabelFrame(self.frame2,           text = "Création")
		self.label_create_taille 			= Label(self.create_planets_frame,  text = "Taille")
		self.create_taille 					= Entry(self.create_planets_frame,  textvariable = self.custom_taille)
		self.label_create_distance 			= Label(self.create_planets_frame,  text = "Distance")
		self.create_distance 				= Entry(self.create_planets_frame,  textvariable = self.custom_distance)
		self.label_create_vitesse 			= Label(self.create_planets_frame,  text = "Vitesse")
		self.create_vitesse 				= Entry(self.create_planets_frame,  textvariable = self.custom_vitesse)
		self.label_create_nom 				= Label(self.create_planets_frame,  text = "Nom")
		self.create_nom 					= Entry(self.create_planets_frame,  textvariable = self.custom_nom)
		self.bouton_create 					= Button(self.create_planets_frame, text = "Créer", 
															     		command = self.ajouter_planete)


		self.predef_planets_frame 			= LabelFrame(self.frame2,           text = "Planet predef")
		self.bouton_create_terre 			= Button(self.predef_planets_frame, text = "T", command = self.ajouter_planete_terre)
		self.bouton_create_soleil   		= Button(self.predef_planets_frame, text = "S", command = self.ajouter_planete_soleil)

		# Placements widgets
		self.frame1.grid 					(row = 0, column = 0)

		self.canvas.grid 					(row = 0, column = 0)

		self.frame2.grid 					(row = 0, column = 1)

		self.reglages_frame.grid 			(row = 0, column = 0)
		self.label_time_spinbox.grid		(row = 0, column = 0, sticky = W)
		self.time_spinbox.grid 				(row = 0, column = 1)

		self.select_planets_frame.grid 		(row = 1, column = 0)

		self.create_planets_frame.grid 		(row = 2, column = 0)
		self.label_create_taille.grid 		(row = 0, column = 0, sticky = W)
		self.create_taille.grid 			(row = 0, column = 1)
		self.label_create_distance.grid 	(row = 1, column = 0, sticky = W)
		self.create_distance.grid 			(row = 1, column = 1)
		self.label_create_vitesse.grid 		(row = 2, column = 0, sticky = W)
		self.create_vitesse.grid 			(row = 2, column = 1)
		self.label_create_nom.grid 			(row = 3, column = 0, sticky = W)
		self.create_nom.grid 				(row = 3, column = 1)
		self.bouton_create.grid 			(row = 4, column = 0, columnspan = 2)

		self.predef_planets_frame.grid 		(row = 3, column = 0)
		self.bouton_create_terre.grid 		(row = 0, column = 0)
		self.bouton_create_soleil.grid 		(row = 1, column = 0)

		# Variables de simulation
		self.planetes 						= []


	def select_planets(self, planetes):
		for planete in planetes:
			self.ajouter_planete 	(planete)

	def ajouter_planete_terre(self):
		self.custom_taille.set 		(50)
		self.custom_distance.set 	(1.2)
		self.custom_vitesse.set 	(1)
		self.custom_nom.set 		("Terre")
		self.ajouter_planete 		(1, 0)

	def ajouter_planete_soleil(self):
		self.custom_taille.set 		(100)
		self.custom_distance.set 	(0)
		self.custom_vitesse.set 	(0)
		self.custom_nom.set 		("Soleil")
		self.ajouter_planete 		(0, 1)


	# Methodes
	def time(self):
		global TIMESPEED
		#print TIMESPEED
		# Update du temps
		TIMESPEED 		= self.time_reglage.get()
		# Incrémenter compteur temps
		time_actualise 	(TIMESPEED)

		# Recommencez après 5 ms
		self.after 		(5, self.time)



	def animation(self):
		compteur = 0
		while compteur < len(self.selected_planetes):

			planete 						= self.selected_planetes[compteur]

			self.canvas.delete 				(planete.pyimage)
			self.canvas.delete 				(planete.nom_pyimage)

			planete.actualiser_position 	(force = True)

			planete.pyimage 				= self.canvas.draw_planet(planete)
			planete.nom_pyimage 			= self.canvas.create_text(planete.get_pos()[0] - len(planete.nom) / 2, 
											  planete.get_pos()[1] - planete.taille / 2 - HEIGHT / 35, 
											  text = planete.nom, fill = "#ffffff")

			compteur += 1

		self.canvas.update_idletasks()
		self.after(6, self.animation)



	def ajouter_planete(self, terre = false, soleil = false):

		# Si le nom de la planète est déjà pris
		if self.custom_nom.get() in self.planetes_noms:
			# On affiche une erreur
			Error_Window	(self, message = "{} existe déjà.".format(self.custom_nom.get()))
			return 1

		# On crée la planète correspondante aux données du GUI
		planete 						= Planete(self.custom_nom.get(), 
						  					float(self.custom_taille.get()), 
						  					float(self.custom_distance.get()), 
						  					float(self.custom_vitesse.get()))
		if terre:
			planete.bleu 				= 255
		elif soleil:
			planete.rouge 				= 255
		else:
			planete.bleu 				= 255
			planete.rouge 				= 255
			planete.vert 				= 255

		equation 						= (planete.distanceUA * cos(planete.vitesseAng * x),
							 	 		  planete.distanceUA * sin(planete.vitesseAng * x))
		planete.set_equation			(equation[0], equation[1])

		# On l'ajoute à la liste des planetes
		self.planetes.append 			(planete)
		self.selected_planetes.append 	(planete)
		# On crée le bouton associé à la planète
		self.ajouter_bouton_planete 	(planete)


	def ajouter_bouton_planete(self, planete):

		self.planetes_noms.append		(planete.nom)
		# On ajoute un nouveau bouton à la fenêtre
		self.boutons_planetes.append	(Planete_Bouton(self.select_planets_frame, planete, len(self.boutons_planetes)))
		# On affiche le bouton
		self.boutons_planetes[-1].show()

	def refresh_planetes(self):
		for bouton in self.boutons_planetes:
			# Si la planète est à cacher
			if not bouton.affiche and bouton.est_affiche:
				self.selected_planetes.remove 	(bouton.planete)
				bouton.est_affiche 				= False
				self.canvas.delete 				(bouton.planete.pyimage)
			# Si la planete est à réafficher
			elif bouton.affiche and not bouton.est_affiche:
				self.selected_planetes.append 	(bouton.planete)
				bouton.est_affiche 				= True
			# Si la planète est à supprimer
			elif bouton.to_delete:
				self.selected_planetes.remove	(bouton.planete)
				self.planetes.remove 			(bouton.planete)
				boutons_planetes.remove 		(bouton)
				bouton.destroy					()

		self.after 								(16, self.refresh_planetes)

	def update(self):
		pass

	def run(self):
		self.time 				()
		self.animation 			()
		self.refresh_planetes	()
		self.update 			()

def main():

	process = Application 	()
	process.initApp 		()

	process.run 			()

	process.mainloop 		()

	return 0

main()
