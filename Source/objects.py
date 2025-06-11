import json
from copy import copy, deepcopy

class Exercitiu:
	def __init__(self, enunt, rasp):
		self.enunt = enunt
		self.raspunsuri_corecte = rasp
		self.raspunsuri_user = []

class Subiect:
	def __init__(self, path):

		self.exercitii = []

		with open(path, 'r') as file:
			data = json.load(file)

			for i in data:
				ex = Exercitiu(data[i]["Enunt"], data[i]["Raspunsuri"])
				ex.raspunsuri_user = []

				self.exercitii.append(ex)
