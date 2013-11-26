# -*-coding:UTF8-*-

print("Test")

REGLE = {'S': {'NP VP': 1}, 'VP' : {'V' : 0.25 , 'V Adv' : 0.25 , 'V NP Adv' : 0.25 , 'V S' : 0.25 },'NP' : { 'Det Adj' : 0.25 , 'Det Adj N' : 0.25, 'Det Adj N N' : 0.25 , 'N' : 0.25 } }
print("Grammaire")
for key in REGLE:
	for key2 in REGLE[key]:
		print(key,' -> ', key2 ," : ",REGLE[key][key2])


for LEFT in REGLE.copy().keys():
	for RIGHT in REGLE[LEFT].copy().keys():
		if len(RIGHT.split( )) == 1:

			#Ajoute une rêgle non terminale A:B
			nouvelle_regle = ":".join([LEFT,RIGHT])
			p1 = REGLE[LEFT][RIGHT]

			#Retire la règle originelle
			del REGLE[LEFT][RIGHT]

			#Modifie la grammaire
			for temp_left in REGLE:
				#Pour toute production de A
				if temp_left == LEFT:
					#Augmente la probabilité pour compenser la supression de A -> B
					for temp_right in REGLE[temp_left]:
						REGLE[temp_left][temp_right] /= (1- p1)
					continue
				#Pour toute production de B
				elif temp_left == RIGHT:
					for temp_right in REGLE[temp_left]:
						if LEFT in temp_right: print("erreur, ",LEFT,"est réécris par ",RIGHT)
						#Assigne à la nouvelle rêgle les mêmes rêgles de réécriture et les mêmes probabilités que celles de B
						REGLE[nouvelle_regle][temp_right]=REGLE[temp_left][temp_right]

				#Pour toutes les autres rêgles de productions C
				for temp_right in REGLE[temp_left].copy().keys():
					#Qui contiennent la rêgle A dans leur réécriture.C -x A y
					if LEFT in temp_right.split( ):
						#Crée une nouvelle rêgle se réécrivant C -> x A:B y
						REGLE[temp_left][" ".join([nouvelle_regle if x==LEFT else x for x in temp_right.split( )])] = p1 * REGLE[temp_left][temp_right]
						#Modifie les probabilités des rêgles contenant A pour en retirer la possibilité de A -> B
						REGLE[temp_left][temp_right] *= (1-p1)

for LEFT in REGLE.copy().keys():
	for RIGHT in REGLE[LEFT].keys():
		if len(RIGHT.split( )) > 2:
			A = RIGHT.split( )
			B = A.pop(len(A)-1)
			nouveau = "-".join(A)
			REGLE[LEFT][" ".join([nouveau,B])] = REGLE[LEFT].pop(RIGHT)
			while len(A) > 1:
				B = A.pop(len(A)-1)
				nouveau2 = "-".join(A)
				REGLE[nouveau] = { " ".join([nouveau2,B]): 1 }
				nouveau = nouveau2


print("Grammaire modifiée")
print(REGLE)
for key in REGLE:
	for key2 in REGLE[key]:
		print(key,' -> ', key2 ," : ",REGLE[key][key2])






