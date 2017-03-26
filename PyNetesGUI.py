# -*- coding: utf-8 -*-
from Tkinter		  import *
from calculs		  import *
from file			  import *
from import_interface import *
from sage.all         import *
import tkMessageBox

centrage 			= False
centrage_planete 	= 0
version 			= "PyNetes (build 24)"

# Du décimal vers de l'héxa.
def conv(chiffre):
	if chiffre > 255 or chiffre < 0:
		return "FF"
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
	x     = planete.get_pos()[0] * zoom + origin[0] 
	y     = planete.get_pos()[1] * zoom + origin[1]
	r     = planete.taille * zoom
	color = "#" + conv(planete.rouge) + conv(planete.vert) + conv(planete.bleu)
	return self.create_oval(x-r, y-r, x+r, y+r, fill = color)
Canvas.draw_planet = _draw_planet

def _draw_trajectoire(self, planete, origin, zoom):
	r     = planete.distanceUA * getUA() * zoom
	x     = fvalue(planete.equationx, 0) * zoom + origin[0]
	y     = fvalue(planete.equationy, 0) * zoom + origin[1]
	color = "#DDDDDD"
	return self.create_oval(x-r, y-r, x+r, y+r, fill = '', width = 0.5, outline = color)
Canvas.draw_trajectoire = _draw_trajectoire	

class Planete_Prop_Window(Toplevel):
	def __init__(self, master, planete, bouton, root):
		Toplevel.__init__(self)

		global centrage_planete

		self.master                     = master
		self.root 					    = root
		self.planete 					= planete
		self.planete_name  				= Label(master = self, text = planete.nom)

		# Affichage
		self.title						("Propriete de " + self.planete.nom)
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

		self.centrea 					= IntVar()


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

		self.goto                       = Checkbutton(self, text = "Centrer", variable = self.centrea, foreground = "#ffffff", selectcolor= "#000000")
		self.goto.grid                  (row = 10, column = 0, columnspan = 2)	

		if self.planete == centrage_planete:
				self.centrea.set(1)	

		self.refresh()

	def refresh(self):
		global centrage
		global centrage_planete
		global version

		try:
			self.planete.rouge 				= self.boutonrouge.get()
		except ValueError:
			self.planete.rouge 				= 0

		try:
			self.planete.vert 				= self.boutonvert.get()
		except ValueError:
			self.planete.vert 				= 0

		try:
			self.planete.bleu 				= self.boutonbleu.get()
		except ValueError:
			self.planete.bleu 				= 0

		self.posx.set 						("Position x : {0:0.1f}".format(float(self.planete.get_pos()[0])))
		self.posy.set 						("Position y : {0:0.1f}".format(float(self.planete.get_pos()[1])))
		try:
			self.planete.taille 			= self.planete_taille.get()
		except ValueError:
			self.planete.taille 			= 0
		
		if(self.centrea.get()):
			centrage 						= True
			centrage_planete 				= self.planete
		else:
			if self.planete == centrage_planete:
				centrage 					= False
				self.root.title				(version)

		self.after 							(30, self.refresh)

class Planete_Bouton(Button):

	def __init__(self, master, planete, length, root):
		Button.__init__(self, master = master)

		# Fenêtre principale
		self.root 			= root

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

		self.grid			(row = length-length%3, column = length%3)

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
		self.to_delete 	 = True
		self.affiche  	 = False

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

		global centrage_planete
		global version
		
		# Self config
		self.tk_setPalette(background='#2d2d30', foreground='#ececec',
			   activeBackground='#212123', activeForeground="#ffffff")

		# Toolbar
		self.toolbar_frame 					= Frame()

		self.menubar 						= Menu(self)
		self.config							(menu = self.menubar)
		self.importmenu 					= Menu(self.menubar)
		self.importmenu.add_command			(label = "Importer depuis un fichier", command = self.import_window)
		self.viewmenu   = Menu				(self.menubar)
		self.viewmenu.add_command			(label = "Reset Zoom",     command = self.reset_zoom)
		self.viewmenu.add_command			(label = "Reset Centrage", command = self.reset_centrage)
		self.astresmenu = Menu				(self.menubar)
		self.astresmenu.add_command			(label = "Voir détails astres", command = self.afficheDetailsAstres)

		self.menubar.add_cascade			(label = "Importation", menu = self.importmenu)
		self.menubar.add_cascade			(label = "View",        menu = self.viewmenu  )
		self.menubar.add_cascade			(label = "Astres",      menu = self.astresmenu  )

		self.toolbar_frame.grid				(row = 0, column = 0, columnspan = 2)
		self.title							(version)

		# Frames canvas et liste des planètes
		self.frame1 						= Frame()
		self.frame2 						= Frame()
		
		self.WIDTH 							= 900
		self.HEIGHT 						= 700
		self.ORIGIN 						= (self.WIDTH / 2, self.HEIGHT / 2)
		self.canvas 						= Canvas(self.frame1, 
													 width = self.WIDTH, 
													 height = self.HEIGHT, 
													 bg = "#000000")  # black background

		self.fond 							= PhotoImage(file="Images/background.png")
		self.fondPyimage 					= self.canvas.create_image		(self.ORIGIN[0], self.ORIGIN[1], image = self.fond)                      

		# Variables
		self.terre_select 					= IntVar()
		self.satelite_select 				= IntVar()
		self.time_reglage 					= IntVar()
		self.UA_reglage                     = IntVar()
		self.zoom_rapide                    = IntVar()
		self.zoom_lent                      = IntVar()
		self.custom_taille 					= StringVar()
		self.custom_distance 				= StringVar()
		self.custom_vitesse 				= StringVar()
		self.custom_nom 					= StringVar()
		self.commande 						= StringVar()

		# Frame des reglages
		self.reglages_frame 				= LabelFrame(self.frame2, text = "Configurations", borderwidth = 3, padx = 5, pady = 5)
		self.label_time_spinbox 			= Label(self.reglages_frame,  text = "Vitesse x ")
		self.time_spinbox   				= Spinbox(self.reglages_frame, from_ = -100000000000, to = 100000000000, textvariable = self.time_reglage)
		self.time_reglage.set 				(1)
		self.label_UA_spinbox 			    = Label(self.reglages_frame,  text = "UA (pixels)")
		self.UA_spinbox   				    = Spinbox(self.reglages_frame, from_ = 1, to = 2000, textvariable = self.UA_reglage)
		self.UA_reglage.set 				(UA)
		# Reglages trajectoire
		self.afficherTrajectoire            = IntVar()
		self.afficherTrajectoire.set        (1)
		self.boutonAfficherTrajectoire      = Checkbutton(self.reglages_frame, text = "Afficher trajectoire", variable = self.afficherTrajectoire, foreground = "#ffffff", selectcolor= "#000000")

		# Frame de sélection des planètes pour affichage
		self.select_planets_frame 			= LabelFrame(self.frame2, borderwidth = 3, text="Astres", pady = 5)
		self.planetes 						= []
		self.boutons_planetes 				= []
		self.selected_planetes 				= []
		self.planetes_noms    				= []

		# Frame de création des planètes
		self.create_planets_frame 			= LabelFrame(self.frame2,           text = "Création", borderwidth = 3, padx = 5, pady = 5)
		self.label_create_nom 				= Label(self.create_planets_frame,  text = "Nom")
		self.create_nom 					= Entry(self.create_planets_frame,  textvariable = self.custom_nom)
		self.label_create_taille 			= Label(self.create_planets_frame,  text = "Taille")
		self.create_taille 					= Entry(self.create_planets_frame,  textvariable = self.custom_taille)
		self.label_create_distance 			= Label(self.create_planets_frame,  text = "Distance")
		self.create_distance 				= Entry(self.create_planets_frame,  textvariable = self.custom_distance)
		self.label_create_vitesse 			= Label(self.create_planets_frame,  text = "Vitesse")
		self.create_vitesse 				= Entry(self.create_planets_frame,  textvariable = self.custom_vitesse)
		self.bouton_create 					= Button(self.create_planets_frame, text = "Créer", 
																 		command = self.ajouter_planete)
		self.bind 							("<Return>", self.ajouter_planete)

		# Reglages zoom
		self.frame_zoom 					= LabelFrame(self.reglages_frame, text = "Vitesse zoom", borderwidth = 3, padx = 5, pady = 5)
		self.b_zoom_rapide 					= Checkbutton(self.frame_zoom, text = "Rapide", variable = self.zoom_rapide, foreground = "#ffffff", selectcolor= "#000000")
		self.b_zoom_lent 					= Checkbutton(self.frame_zoom, text = "Lent", variable = self.zoom_lent, foreground = "#ffffff", selectcolor= "#000000")

		# Placements widgets
		self.frame1.grid 					(row = 1, column = 0)

		self.canvas.grid 					(row = 0, column = 0)

		self.frame2.grid 					(row = 1, column = 1)

		self.reglages_frame.grid 			(row = 0, column = 0)
		self.label_time_spinbox.grid		(row = 0, column = 0, sticky = W)
		self.time_spinbox.grid 				(row = 0, column = 1)
		self.label_UA_spinbox.grid          (row = 1, column = 0, sticky = W)
		self.UA_spinbox.grid                (row = 1, column = 1)
		self.boutonAfficherTrajectoire.grid (row = 3, column = 0, columnspan = 2)

		self.select_planets_frame.grid 		(row = 1, column = 0)

		self.create_planets_frame.grid 		(row = 2, column = 0)
		self.label_create_nom.grid 			(row = 0, column = 0, sticky = W)
		self.create_nom.grid 				(row = 0, column = 1)
		self.label_create_taille.grid 		(row = 1, column = 0, sticky = W)
		self.create_taille.grid 			(row = 1, column = 1)
		self.label_create_distance.grid 	(row = 2, column = 0, sticky = W)
		self.create_distance.grid 			(row = 2, column = 1)
		self.label_create_vitesse.grid 		(row = 3, column = 0, sticky = W)
		self.create_vitesse.grid 			(row = 3, column = 1)
		self.bouton_create.grid 			(row = 4, column = 0, columnspan = 2)

		self.frame_zoom.grid				(row = 2, column = 0, columnspan = 2)
		self.b_zoom_rapide.grid				(row = 0, column = 0)
		self.b_zoom_lent.grid				(row = 0, column = 1)

		# UI id
		self.echelleUA       				= -1
		self.echelleUAlimits 				= [-1, -1]
		self.echelleUAlabel  				= -1

		self.originLabel    				= -1
		self.timeLabel       				= -1
		 

		# Variables de simulation
		self.planetes 						= []
		self.zoom                           = 1 # 100%

		# Binds
		self.canvas.is_focus 				= False
		self.canvas_binds					()

		# Pour redimentionner la fenètre !
		self.update_idletasks				()
		self.old_taillex 					= self.winfo_width()
		self.old_tailley 					= self.winfo_height()

	""" Initialise les commandes sur le canvas """
	def canvas_binds(self):
		self.canvas.focus_set	()

		# focuses
		self.canvas.bind 		("<Enter>",  self.focus)
		self.canvas.bind 		("<Leave>",  self.unfocus)

		# Zoom
		self.bind 				("<Button-4>", lambda event : self.change_zoom(event)) # scroll up
		self.bind 				("<Button-5>", lambda event : self.change_zoom(event)) # scroll down

		# move
		self.canvas.bind 		("<Button-1>",   lambda event : self.start_movein(event))
		self.canvas.bind 		("<B1-Motion>",  lambda event : self.end_movein(event))     # Mouvement dans le canvas

	# Commandes
	""" focus le canvas pour le zoom """
	def focus(self, event):
		self.canvas.is_focus 	= True

	""" unfocus le canvas pour interdire le zoom """
	def unfocus(self, event):
		self.canvas.is_focus 	= False

	def start_movein(self, event):
		self.movex 				= event.x
		self.movey 				= event.y

	def end_movein(self, event):
		global centrage
		global version
		centrage 				= False
		self.title				(version)
		origin0 				= self.ORIGIN[0] + (event.x - self.movex)
 		origin1 				= self.ORIGIN[1] + (event.y - self.movey)
		self.ORIGIN 			= (origin0, origin1)
		self.movex 				= event.x
		self.movey 				= event.y

	def change_zoom(self, event):
		if(not self.canvas.is_focus):
			return 1
		if self.zoom_lent.get() == 1:
			modif1 	= 0.02
		elif self.zoom_rapide.get() == 1:
			modif1 	= 0.5
		else:
			modif1 	= 0.1
		modif 		= 0

		if event.num == 5 or event.delta == -120:
			modif -= modif1
		elif event.num == 4 or event.delta == 120:
			modif += modif1
		else:
			pass

		if(self.zoom + modif <= 0):
			self.zoom = 0.02
		else:
			self.zoom += modif

	def reset_zoom(self):
		self.zoom = 1
		return self.zoom

	def reset_centrage(self):
		global centrage
		centrage 	= False
		self.ORIGIN = (self.WIDTH / 2, self.HEIGHT / 2)


	# Methodes

	def time(self):
		global TIMESPEED
		#print TIMESPEED
		# Update du temps
		try:
			TIMESPEED 		= self.time_reglage.get()
		except ValueError:
			TIMESPEED 		= 0
		# Incrémenter compteur temps
		time_actualise 		(TIMESPEED)

		# Recommencez après 5 ms
		self.after 			(5, self.time)

	def animation(self):

		self.refresh_UI						()

		compteur							= 0
		while compteur < len(self.selected_planetes):

			planete 						= self.selected_planetes[compteur]

			self.canvas.delete 				(planete.pyimage)
			self.canvas.delete 				(planete.nom_pyimage)

			if(self.afficherTrajectoire.get()):
				self.canvas.delete          (planete.trajectoire)
				planete.trajectoire         = self.canvas.draw_trajectoire(planete, self.ORIGIN, self.zoom)

			planete.actualiser_position 	()

			planete.pyimage 				= self.canvas.draw_planet(planete, self.ORIGIN, self.zoom)

			x 								= planete.get_pos()[0] * self.zoom + self.ORIGIN[0] - (len(planete.nom) / 2)
			y 								= planete.get_pos()[1] * self.zoom + self.ORIGIN[1] - planete.taille * self.zoom - self.HEIGHT / 35

			planete.nom_pyimage 			= self.canvas.create_text(x, y, text = planete.nom, fill = "#ffffff")
											  
			compteur 						+= 1

		self.canvas.update_idletasks		()

		self.after 							(6, self.animation)

	def ajouter_planete(self, importedPlanete = False):

		# Si le nom de la planète est déjà pris
		if self.custom_nom.get() in self.planetes_noms:
			# On affiche une erreur
			tkMessageBox.showwarning 		("Nom invalide", "{} existe déjà.".format(self.custom_nom.get()))
			return 1
		elif importedPlanete.nom in self.planetes_noms: # Permet l'import "tout" sans avoir à retirer les planètes préexistantes
			return 1

		# On crée la planète correspondante aux données du GUI
		if not importedPlanete:
			planete 						= Planete(self.custom_nom.get(), 
						  						float(self.custom_taille.get()), 
						  						float(self.custom_distance.get()), 
						  						float(self.custom_vitesse.get()))
		else:
			planete = importedPlanete

		equation 							= (planete.distanceUA * cos(planete.vitesseAng * x),
							 	 			   planete.distanceUA * sin(planete.vitesseAng * x))
		planete.set_equation				(equation[0], equation[1])

		# On l'ajoute à la liste des planetes
		self.planetes.append 				(planete)
		self.selected_planetes.append 		(planete)
		# On crée le bouton associé à la planète
		self.ajouter_bouton_planete 		(planete)

	def ajouter_bouton_planete(self, planete):

		self.planetes_noms.append			(planete.nom)
		# On ajoute un nouveau bouton à la fenêtre
		self.boutons_planetes.append		(Planete_Bouton(self.select_planets_frame, planete, len(self.boutons_planetes), self))
		# On affiche le bouton
		self.boutons_planetes[-1].show 		()

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

	""" Appelé par animation avant l'affichage des planètes """
	def refresh_UI(self):
		global UA
		global years
		global centrage
		global centrage_planete
		global version

		le_super_nouveau_WIDTH 		= self.winfo_width() - self.old_taillex + self.WIDTH
		le_super_nouveau_HEIGHT 	= self.winfo_height() - self.old_tailley + self.HEIGHT

		self.canvas.config			(width = le_super_nouveau_WIDTH, height = le_super_nouveau_HEIGHT)

		self.WIDTH 					= le_super_nouveau_WIDTH
		self.HEIGHT 				= le_super_nouveau_HEIGHT
		self.old_taillex 			= self.winfo_width()
		self.old_tailley 			= self.winfo_height()
		

		if centrage:
			centrage_ori_x 			= - (centrage_planete.get_pos()[0] * self.zoom) + self.WIDTH  / 2
			centrage_ori_y 			= - (centrage_planete.get_pos()[1] * self.zoom) + self.HEIGHT / 2
			self.ORIGIN 			= (centrage_ori_x, centrage_ori_y)
			self.title				(version + " : " + centrage_planete.nom + " : Position : (" + str(centrage_ori_x) + ", "+ str(centrage_ori_y) + ")")

		liste 						= [self.echelleUA, self.echelleUAlimits, self.echelleUAlabel, 
		   							   self.originLabel, self.timeLabel, self.fondPyimage]

		# deletes
		for id in liste:
			if type(id) == tuple or type(id) == list:
				for subid in id:
					self.canvas.delete					(subid)
			else:
				self.canvas.delete						(id)

		self.fondPyimage = self.canvas.create_image		(self.ORIGIN[0], self.ORIGIN[1], image = self.fond)

		# Afficher échelle UA
		try:
			setUA                                   	(self.UA_reglage.get())
		except ValueError:
			setUA                                    	(0)
		self.echelleUA = self.canvas.create_line     	(self.WIDTH / 20, self.HEIGHT / 50,
													 	 self.WIDTH / 20 + UA * self.zoom, 
														 self.HEIGHT / 50,
													  	 fill = "#ffffff")
		self.echelleUAlimits = [
			self.canvas.create_line                  	(self.WIDTH / 20, self.HEIGHT / 60, 
													  	 self.WIDTH / 20, self.HEIGHT / 40, fill = "#ffffff"),
			self.canvas.create_line                  	(self.WIDTH / 20 + UA * self.zoom, self.HEIGHT / 60, 
														 self.WIDTH / 20 + UA * self.zoom, self.HEIGHT / 40, fill = "#ffffff")
			]
		self.echelleUAlabel = self.canvas.create_text	((self.WIDTH / 20 + (self.WIDTH / 20 + UA * self.zoom)) / 2, self.HEIGHT / 25,
													  	  text = "UA", fill = "#ffffff", font = "LucidaConsole 12")
		# Afficher origine

		self.originLabel = self.canvas.create_text   	(self.WIDTH / 50, self.HEIGHT - self.HEIGHT / 50,
													  	 text = "Origine : ( {} ; {} )".format(self.ORIGIN[0], self.ORIGIN[1]),
													  	 fill = "#ffffff", anchor = W)

		# Afficher temps
		self.timeLabel = self.canvas.create_text     	(self.WIDTH - len("Années passées : ")*3 - len(str(return_year()))*4, self.HEIGHT - self.HEIGHT / 50,
													  	 text = "Années passées : {}".format(return_year()), fill = "#ffffff")

	def import_window(self):

		self.importAnswer 			= ImportWindow().show()
		self.get_imported_planetes	()

	def get_imported_planetes(self):

		if(not self.importAnswer == 0):
			for planete in self.importAnswer:
				# On crée les planètes
				self.ajouter_planete(planete)

	def afficheDetailsAstres(self):

		for bouton in self.boutons_planetes:
			bouton.afficher_fenetre()

	def run(self):
		self.time 				()
		self.animation 			()
		self.refresh_planetes	()

def main():

	process = Application 	()

	process.run 			()

	process.mainloop 		()

	return 0

main()
0
