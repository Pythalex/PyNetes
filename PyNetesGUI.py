# -*- coding: utf-8 -*-
from Tkinter		  import *
from calculs		  import *
from file			  import *
from import_interface import *
from sage.all         import *
import tkMessageBox

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

def _draw_planet(self, planete, origin, zoom):
	#print(planete.get_pos()[0] / UAKM * zoom + origin[0])
	#print(planete.get_pos()[1] / UAKM * zoom + origin[1])
	x    = planete.get_pos()[0] * zoom + origin[0] 
	y    = planete.get_pos()[1] * zoom + origin[1]
	r    = planete.taille * zoom
	color = "#" + conv(planete.rouge) + conv(planete.vert) + conv(planete.bleu)
	return self.create_oval(x-r, y-r, x+r, y+r, fill = color)
Canvas.draw_planet = _draw_planet

class Planete_Prop_Window(Toplevel):

	def __init__(self, master, planete, bouton, root):
		Toplevel.__init__(self)
		self.master                     = master
		self.root 					    = root
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
		self.planete_taille_value		= Spinbox(master = self, from_ = 0.001, to    = 10000000000000000, 
									              textvariable = self.planete_taille)


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

		self.goto                       = Button(self, text = "Centrer", command = self.centrer)
		self.goto.grid                  (row = 9, column = 0, columnspan = 2)

		self.refresh()

	def refresh(self):
		self.planete.rouge 				= self.boutonrouge.get()
		self.planete.vert 				= self.boutonvert.get()
		self.planete.bleu 				= self.boutonbleu.get()
		self.posx.set 					("Position x : {0:0.1f}".format(float(self.planete.get_pos()[0])))
		self.posy.set 					("Position y : {0:0.1f}".format(float(self.planete.get_pos()[1])))

		self.planete.taille 			= self.planete_taille.get()

		self.after 						(30, self.refresh)

	def centrer(self):
		origin0 = self.root.ORIGIN[0] - self.planete.get_pos()[0]
		origin1 = self.root.ORIGIN[1] - self.planete.get_pos()[1]
		self.root.ORIGIN = (origin0, origin1)

class Planete_Bouton(Button):

	def __init__(self, master, planete, length, root):
		Button.__init__(self, master = master)

		# Fenêtre principale
		self.root = root

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
		Planete_Prop_Window(self.master, self.planete, self, self.root)

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

class Application(Tk):

	# Initialisations
	def __init__(self):

		Tk.__init__(self)

		# Self config
		self.tk_setPalette(background='#2d2d30', foreground='#ececec',
               activeBackground='#212123', activeForeground="#ffffff")

		# Toolbar
		self.toolbar_frame = Frame()

		self.menubar = Menu(self)
		self.config(menu = self.menubar)
		self.importmenu = Menu(self.menubar)
		self.importmenu.add_command(label = "import from file", command = self.import_window)
		self.menubar.add_cascade(label = "Import", menu = self.importmenu)

		self.toolbar_frame.grid(row = 0, column = 0, columnspan = 2)

		# Frames canvas et liste des planètes
		self.frame1 						= Frame()
		self.frame2 						= Frame()
		
		self.WIDTH = 800
		self.HEIGHT = 600
		self.ORIGIN = (self.WIDTH / 2, self.HEIGHT / 2)
		self.canvas 						= Canvas(self.frame1, 
													 width = self.WIDTH, 
													 height = self.HEIGHT, 
													 bg = "#000000")  # black background                      

		# Variables
		self.terre_select 					= IntVar()
		self.satelite_select 				= IntVar()
		self.custom_taille 					= StringVar()
		self.custom_distance 				= StringVar()
		self.custom_vitesse 				= StringVar()
		self.custom_nom 					= StringVar()
		self.time_reglage 					= IntVar()
		self.UA_reglage                     = IntVar()

		# Frame des reglages
		self.reglages_frame 				= LabelFrame(self.frame2, text = "Configurations", borderwidth = 0, padx = 5, pady = 5)
		self.label_time_spinbox 			= Label(self.reglages_frame,  text = "Temps (x mult)")
		self.time_spinbox   				= Spinbox(self.reglages_frame, from_ = -100000000000, to = 100000000000, textvariable = self.time_reglage)
		self.time_reglage.set 				(1)
		self.label_UA_spinbox 			    = Label(self.reglages_frame,  text = "UA (pixels)")
		self.UA_spinbox   				    = Spinbox(self.reglages_frame, from_ = 1, to = 2000, textvariable = self.UA_reglage)
		self.UA_reglage.set 				(UA)

		# Frame de sélection des planètes pour affichage
		self.select_planets_frame 			= LabelFrame(self.frame2, text="Planètes", pady = 5)
		self.planetes 						= []
		self.boutons_planetes 				= []
		self.selected_planetes 				= []
		self.planetes_noms    				= []

		# Frame de création des planètes
		self.create_planets_frame 			= LabelFrame(self.frame2,           text = "Création", borderwidth = 0, padx = 5, pady = 5)
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


		self.predef_planets_frame 			= LabelFrame(self.frame2,           text = "Planet predef", borderwidth = 0, padx = 5, pady = 5)

		# Placements widgets
		self.frame1.grid 					(row = 1, column = 0)

		self.canvas.grid 					(row = 0, column = 0)

		self.frame2.grid 					(row = 1, column = 1)

		self.reglages_frame.grid 			(row = 0, column = 0)
		self.label_time_spinbox.grid		(row = 0, column = 0, sticky = W)
		self.time_spinbox.grid 				(row = 0, column = 1)
		self.label_UA_spinbox.grid          (row = 1, column = 0, sticky = W)
		self.UA_spinbox.grid                (row = 1, column = 1)

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

		# UI id
		self.echelleUA       = -1
		self.echelleUAlimits = [-1, -1]
		self.echelleUAlabel  = -1

		self.originLabel     = -1
		self.timeLabel       = -1
		 

		# Variables de simulation
		self.planetes 						= []
		self.zoom                           = 1 # 100%

		# Binds
		self.canvas.is_focus = False
		self.canvas_binds()

	""" Initialise les commandes sur le canvas """
	def canvas_binds(self):
		self.canvas.focus_set()

		# focuses
		self.canvas.bind("<Enter>",  self.focus)
		self.canvas.bind("<Leave>",  self.unfocus)

		# Zoom
		self.bind("<MouseWheel>", lambda event : self.change_zoom(event)) # windows scroll up & down
		self.bind("<Button-4>",   lambda event : self.change_zoom(event)) # Linux   scroll up
		self.bind("<Button-5>",   lambda event : self.change_zoom(event)) # Linux   scroll down

		# move
		self.canvas.bind("<Button-1>",   lambda event : self.start_movein(event))
		self.canvas.bind("<B1-Motion>",  lambda event : self.end_movein(event))     # Mouvement dans le canvas
		# self.canvas.bind("<B1-Motion>", command = )

	# Commandes
	""" focus le canvas pour le zoom """
	def focus(self, event):
		self.canvas.is_focus = True

	""" unfocus le canvas pour interdire le zoom """
	def unfocus(self, event):
		self.canvas.is_focus = False

	def start_movein(self, event):
		self.movex = event.x
		self.movey = event.y

	def end_movein(self, event):
		origin0 = self.ORIGIN[0] + (event.x - self.movex)
		origin1 = self.ORIGIN[1] + (event.y - self.movey)
		self.ORIGIN = (origin0, origin1)
		self.movex = event.x
		self.movey = event.y

	def change_zoom(self, event):
		if(not self.canvas.is_focus):
			return 1
		modif = 0
		# Gerer les events linux et windows
		if event.num == 5 or event.delta == -120:
			modif -= 0.1
		elif event.num == 4 or event.delta == 120:
			modif += 0.1
		else:
			pass
		if(self.zoom + modif <= 0):
			self.zoom = 0.1
		else:
			self.zoom += modif


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

			planete.actualiser_position 	()

			planete.pyimage 				= self.canvas.draw_planet(planete, self.ORIGIN, self.zoom)

			x = planete.get_pos()[0] * self.zoom + self.ORIGIN[0] - (len(planete.nom) / 2)
			y = planete.get_pos()[1] * self.zoom + self.ORIGIN[1] - planete.taille * self.zoom - self.HEIGHT / 35

			planete.nom_pyimage 			= self.canvas.create_text(x, y, text = planete.nom, fill = "#ffffff")
											  
			compteur += 1

		self.canvas.update_idletasks()
		self.after(6, self.animation)

	def ajouter_planete(self):

		# Si le nom de la planète est déjà pris
		if self.custom_nom.get() in self.planetes_noms:
			# On affiche une erreur
			tkMessageBox.showwarning("Nom invalide", 
						  "{} existe déjà.".format(self.custom_nom.get()))
			return 1

		# On crée la planète correspondante aux données du GUI
		planete 						= Planete(self.custom_nom.get(), 
						  					float(self.custom_taille.get()), 
						  					float(self.custom_distance.get()), 
						  					float(self.custom_vitesse.get()))

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
		self.boutons_planetes.append	(Planete_Bouton(self.select_planets_frame, planete, len(self.boutons_planetes), self))
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

	def refresh_UI(self):
		global UA
		global years

		liste = [self.echelleUA, self.echelleUAlimits, self.echelleUAlabel, 
		   self.originLabel, self.timeLabel]

		# deletes
		for id in liste:
			if type(id) == tuple or type(id) == list:
				for subid in id:
					self.canvas.delete(subid)
			else:
				self.canvas.delete(id)

		# Afficher échelle UA
		setUA(self.UA_reglage.get())
		self.echelleUA = self.canvas.create_line(self.WIDTH / 20, self.HEIGHT / 50,
												 self.WIDTH / 20 + UA * self.zoom, 
												 self.HEIGHT / 50,
												 fill = "#ffffff")
		self.echelleUAlimits = [
			self.canvas.create_line(self.WIDTH / 20, self.HEIGHT / 60, 
						            self.WIDTH / 20, self.HEIGHT / 40, fill = "#ffffff"),
			self.canvas.create_line(self.WIDTH / 20 + UA * self.zoom, self.HEIGHT / 60, 
						            self.WIDTH / 20 + UA * self.zoom, self.HEIGHT / 40, fill = "#ffffff")
			]
		self.echelleUAlabel = self.canvas.create_text((self.WIDTH / 20 + (self.WIDTH / 20 + UA * self.zoom)) / 2, self.HEIGHT / 25,
													  text = "UA", fill = "#ffffff", font = "LucidaConsole 12")
		# Afficher origine

		self.originLabel = self.canvas.create_text(self.WIDTH / 50, self.HEIGHT - self.HEIGHT / 50,
												   text = "origine : ( {} ; {} )".format(self.ORIGIN[0], self.ORIGIN[1]),
												   fill = "#ffffff", anchor = W)

		# Afficher temps
		self.timeLabel = self.canvas.create_text(self.WIDTH - len("years passed : ")*3 - len(str(years))*4, self.HEIGHT - self.HEIGHT / 50,
												 text = "years passed : {}".format(years), fill = "#ffffff")

		# reload
		self.after(50, self.refresh_UI) 

	def import_window(self):

		self.importAnswer = ImportWindow().show()
		self.get_imported_planetes()

	def get_imported_planetes(self):

		if(not self.importAnswer == 0):
			# On sauvegarde les anciennes valeurs de l'utilisteur
			old_ct = self.custom_taille.get()
			old_d  = self.custom_distance.get()
			old_v  = self.custom_vitesse.get()
			old_n  = self.custom_nom.get()

			for planete in self.importAnswer:
				# On crée les planètes
				self.custom_taille.set 		(planete.taille)
				self.custom_distance.set 	(planete.distanceUA)
				self.custom_vitesse.set 	(planete.vitesseAng)
				self.custom_nom.set 		(planete.nom)

				self.ajouter_planete()

			# On remet les anciennes valeurs
			self.custom_taille.set 		(old_ct)
			self.custom_distance.set 	(old_d)
			self.custom_vitesse.set 	(old_v)
			self.custom_nom.set 		(old_n)


	def run(self):
		self.time 				()
		self.animation 			()
		self.refresh_planetes	()
		self.refresh_UI         ()

def main():

	process = Application 	()

	process.run 			()

	process.mainloop 		()

	return 0

main()
