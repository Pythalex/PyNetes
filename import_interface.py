# -*- coding: utf-8 -*-

from Tkinter import *
import tkMessageBox

import file

class ImportWindow(Toplevel):

	def __init__(self):
		Toplevel.__init__(self)
		self.title("Importation planetes")

		planetes = self.read_file()

		self.boutons_frame = Frame(self)
		self.boutons_frame.grid(row = 0, column = 0,
						  padx = 10, pady = 5)
		self.boutons = [] 

		# Crée un bouton de check pour chaque planète dans le fichier planetes.txt
		for planete in planetes:
			id     = IntVar()
			bouton = Checkbutton(master     = self.boutons_frame,
								 text       = planete.nom,
								 variable   = id,
								 foreground = "#ffffff",
								 selectcolor= "#000000")
			bouton.var = id
			bouton.planete = planete

			self.boutons.append(bouton)

	def show(self):
		row = 0
		for bouton in self.boutons:
			bouton.grid(row = row, column = 0)
			row += 1

		self.bouton_valide = Button(master = self.boutons_frame,
							        text = "Valider",
									command = self.valider)
		self.bouton_valide.grid(row = row, column = 0,
						  columnspan = 2, padx = 5)

		self.importAnswer = 0 # Valeur de retour pour l'application principale

		self.deiconify()
		self.wait_window()
		return self.importAnswer

	def valider(self):
		self.planetes_a_ajouter = []

		# Pour chaque checkbutton dans la fenêtre, si le bouton est on, la planète est ajoutée
		for bouton in self.boutons:
			if bouton.var.get():
				self.planetes_a_ajouter.append(bouton.planete)

		self.importAnswer = self.planetes_a_ajouter
		self.destroy()

	def read_file(self):
		planetes = file.lire_save(filename = "Planetes/planetes.txt")
		return planetes


# debug
if __name__ == "__main__":
	
	root  = Tk()
	root.title("main")
	impw  = ImportWindow()
	print(impw)
	root.mainloop()