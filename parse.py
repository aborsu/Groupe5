#!/usr/bin/env python3
from collections import defaultdict
from tree import *

def parse(sentence,grammar,lexique):
	"""
	Algorithme de parsing de type EARLEY probabiliste.
	L'algorithme prend une phrase, une grammaire et un lexique en entrée et retourne un arbre de probabilité maximale.
	"""

	def add_to_table(tableau,prediction):
		"""
		Vérifi qu'un élément n'est pas dans la table avant de l'ajouter
		"""
		key1 = prediction.head
		key2 = prediction.wants
		if len(tableau[key1][key2]) > 0:
			for element in tableau[key1][key2]:
				if element.name == prediction.name:
					return
			tableau[key1][key2].append(prediction)
		else:
			tableau[key1][key2] = [prediction]

	def predict(tableau,key1,key2):
		"""
		Cette fonction effectue l'étape de prédiction de l'algorithme d'Earley.
		Nous avons 3 arguments.
		Un tableau de prédictions dans lequel les nouvelles rêgle seront rajoutées.
		La tête de la rêgle qui demande une prédiction
		L'élément syntaxique recherché (qui sera donc la tête de la prédiction)
		"""
		for key3 in grammar[key2]:
		#Pour chaque rêgle key3 ayant comme tête key2 dans la grammaire

			# Crée une nouvelle prédiction
			new_prediction = prediction(key2,[],key3.split(' '),i,key1,grammar[key2][key3])
			key4 = new_prediction.wants

			#Ajoute à la table
			add_to_table(tableau,new_prediction)

			#Si key 4 est dans la grammaire (est non terminal, on continue les prédictions)
			if key4 in grammar:
				predict(tableau,key2,key4)

	def shift(tableau1,tableau2,pos):
		mot = sentence[i]
		classe = lexique[mot]

		for key1 in tableau1:
			for element in tableau1[key1][classe]:
				#fait un nouvel élément
				head, before_dot, after_dot, beginning, father,p,sons = element.suivant()
				terminal = prediction(classe,sentence[i],[],i,key1,1)
				terminal.lexique = sentence[i]
				if sons == None:
					sons = [terminal]
				else:
					sons.append(terminal)
				new_prediction = prediction(head,before_dot,after_dot,beginning,father,p,sons)

				add_to_table(tableau2,new_prediction)

	def complete(tableau,element):
		#Si l'élément n'a pas de père (il s'agit du noeud '$SENT') alors la complétion est finie.
		if element.father == None:
			return
		
		#Pour tous les pères possibles dans le tableau ou l'élément à commencé
		for father_el in tableaux[element.beginning][element.father][element.head]:
			
			#Déplace le dot
			head, before_dot, after_dot, beginning, father,p,sons = father_el.suivant()
			
			# sons contient l'ensemble des fils d'un élément
			if sons == None:
				sons = [element]
			else:
				sons.append(element)
			
			new_prediction = prediction(head,before_dot,after_dot,beginning,father,p*element.p,sons)
			
			add_to_table(tableau,new_prediction)

			if new_prediction.wants == "fini":
				complete(tableau,new_prediction)

	def get_subtrees(elements):
		result = []
		for node in elements:
			if node.sons == None :
				tree = Tree(node.head,False)
				lex = Tree(node.lexique,True)
				tree.subtrees = [lex]
				result.append(tree)
			else:
				tree = Tree(node.head,False)
				tree.subtrees = get_subtrees(node.sons)
				result.append(tree)
		# for el in result:
		# 	print(str(el))
		return result
	
	#Première rêgle permettant de produire une phrase
	"""
	Crée une rêgle mettant en rot
	"""
	sent = prediction('$SENT',[],['SENT'],0,None,1)
	
	#Tableaux est une liste de dictionnaire. Chaque dictionnaire donne toute les rêgles possible à son étape.
	tableaux = list()
	for i in range(0,len(sentence)+1):
		tableaux.append(defaultdict(lambda : defaultdict(str)))
	
	#Point 0
	i = 0

	#La première rêgle du tableau est qu'il peut produire une phrase.
	tableaux[i]['$SENT']['SENT'] = [sent]

	#Boucle de traitement
	while i < len(sentence):
		#Phase de prédiction
		for key1 in tableaux[i].copy():
			for key2 in tableaux[i][key1].keys():
				if key2 in grammar: predict(tableaux[i],key1,key2)

		#Shift
		shift(tableaux[i],tableaux[i+1],i)
		i += 1

		#Complétion
		print(i)
		for key1 in tableaux[i].copy():
			if "fini" in tableaux[i][key1]:
				for element in tableaux[i][key1]["fini"]:
					complete(tableaux[i],element)
	

	for pos,tableau in enumerate(tableaux):
		print("\nTableau",pos)
		for key1 in tableau:
			for key2 in tableau[key1]:
				for element in tableau[key1][key2]:
					element.print()

	resultat = []
	for element in tableaux[i]["SENT"]["fini"]:
		sent = Tree("SENT",False)
		sent.subtrees = get_subtrees(element.sons) 
		resultat.append([sent,element.p])
	return resultat	

class prediction:
	def __init__(self,head,before_dot,after_dot,beginning,father,p,sons=None):
		self.name = [head,before_dot,after_dot,p]
		self.head = self.name[0]
		self.before_dot = self.name[1]
		self.after_dot = self.name[2]
		if after_dot == []:
			self.wants = "fini"
		else:
			self.wants = self.name[2][0]
		self.beginning = beginning
		self.father = father
		self.p = p
		self.sons = sons
		self.lexique = False
	
	def suivant(self):
		new_before_dot = self.before_dot.copy()
		new_before_dot.append(self.wants)
		return self.head, new_before_dot, self.after_dot[1:], self.beginning, self.father, self.p, self.sons
		
	def print(self):
		print("".join(["[",str(self.beginning),"]",self.head," -> "," ".join(self.before_dot)," * "," ".join(self.after_dot)])," P = ",self.p)	





if __name__ == "__main__":
	# #Test 1
	# grammaire_test = {'SENT': {'NP VP': 1}, 'VP' : {'V' : 0.25 , 'V Adv' : 0.25 , 'V NP Adv' : 0.25 , 'V S' : 0.25 },'NP' : { 'Det N' : 0.25 , 'Det Adj N' : 0.25, 'Det Adj N N' : 0.25 , 'N' : 0.25 } }
	# phrase_test = ["la","fille","dort"]
	# lexique_test = {'la':'Det','fille':'N','dort':'V'}
	#Test 2
	grammaire_test = {'SENT': {'T c': 1}, 'T' : {'A B' : 0.8 , 'C E' : 0.2},'A' : { 'a' : 1},'B' : {'b b' : 1},'C' : {'a b':1},'E' : {'b':1} }
	phrase_test = ["a","b","b","c"]
	lexique_test = {'a':'a','b':'b','c':'c'}

	print("Test d'un algorithme de type Earley")
	print("===================================")
	print("L'algrithme va maintenant tenter de parser la phrase suivante:")
	print(phrase_test)
	print("au moyen des rêgles de grammaire suivantes")
	for key in grammaire_test:
		for key2 in grammaire_test[key]:
			print(key,' -> ', key2 ," : ",grammaire_test[key][key2])
	print("Et avec le lexique suivant")
	for key in lexique_test:
		print(key, ' : ', lexique_test[key]) 

	resultat = parse(phrase_test,grammaire_test,lexique_test)	
	print()
	print("Analyses résultantes ...")
	for el in resultat:
		print(str(el[0])," avec comme probabilité ", el[1])
	pass
