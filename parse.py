#!/usr/bin/env python3
from collections import defaultdict
from tree import *

def parse(sentence,grammar,lexique):
	"""
	Algorithme de parsing de type EARLEY probabiliste.
	L'algorithme prend une phrase, une grammaire et un lexique en entrée et retourne un arbre de probabilité maximale.
	"""

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
			
			#Regarde si la prédiction est déjà dans la grammaire
			for element in tableau[key2][key4]:
				#S'il s'agit de la même prédiction alors aucune nécessité de garder les deux
				if element.name == new_prediction.name:
					continue
				
				#Il peut y avoir d'autres prédiction qui ont la même tête et veulent le même élément suivant mais ne sont pas identique.
				else:
				#On les rajoute aux mêmes endroit
					tableau[key2][key4].append(new_prediction)
			
			#Si aucune rêgle n'existait à cet endroit on la rajoute
			if len(tableau[key2][key4]) == 0:
				tableau[key2][key4] = [new_prediction]

			#Si key 4 est dans la grammaire (est non terminal, on continue les prédictions)
			if key4 in grammar:
				predict(tableau,key2,key4)


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
			new_element = prediction(head,before_dot,after_dot,beginning,father,p*element.p,sons)
			
			#Rajoute la règle modifiée au tableau
			if head in tableau:
				if new_element.wants in tableau[head]:
					for existing in tableau[head][new_element.wants]:
						if existing.name == new_element.name:
							pass
					else:
						tableau[head][new_element.wants].append(new_element)
				else:
					tableau[head][new_element.wants]=[new_element]
			else:
				tableau.update({head:{new_element.wants : [new_element]}})

			#Si la rêgle est maintenant finie, on continue de compléter
			if new_element.wants == "fini":
				complete(tableau,new_element)
						
	

	#print("Verification")
	#Prière rêgle permettant de produire une phrase
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
				if key2 in grammar:
					predict(tableaux[i],key1,key2)
		#Shift
		j=i
		i += 1
		
		#Imprime le tableau qui vient d'être fini
		print("\nTableau ",j,":" )
		print("ici")
		print(lexique[sentence[j]], sentence[j])
		for key1 in tableaux[j]:
			for key2 in tableaux[j][key1]:			
				#Tant qu'à parcourir le tableau autant en 1profiter pour initialiser le suivant
				if key2 == lexique[sentence[j]]:
					if key1 not in tableaux[i]:
						tableaux[i][key1]={}
					for element in tableaux[j][key1][key2]:
						element.print()
						head, before_dot, after_dot, beginning, father,p,sons = element.suivant()
						lex = prediction(key2,sentence[j],[],j,key1,1)
						lex.lexique = sentence[j]
						if sons == None:
							sons = [lex]
						else:
							sons.append(lex)
						new_element = prediction(head,before_dot,after_dot,beginning,father,p,sons)

						key3 = new_element.wants
						if key3 in tableaux[i][key1]:
							tableaux[i][key1][key3].append(new_element)
						else:
							tableaux[i][key1][key3] = [new_element]								
				else:
					for element in tableaux[j][key1][key2]:
						element.print()

		#Complétion
		for key1 in tableaux[i].copy():
			if "fini" in tableaux[i][key1]:
				for element in tableaux[i][key1]["fini"]:
					complete(tableaux[i],element)
		
	print("\nTableau",i)
	for key1 in tableaux[i]:
		for key2 in tableaux[i][key1]:
			for element in tableaux[i][key1][key2]:
				element.print()

	resultat = []
	for element in tableaux[i]["SENT"]["fini"]:
		sent = Tree("SENT",False)
		sent.subtrees = get_subtrees(element.sons) 
		resultat.append([sent,element.p])
	return resultat

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


	

class prediction:
	def __init__(self,head,before_dot,after_dot,beginning,father,p,sons=None):
		self.name = [head,before_dot,after_dot]
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
