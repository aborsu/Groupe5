#!/usr/bin/env python3
from extraction import *
from parse import *

if __name__ == "__main__" :
	print("Construction des arbres")
	ftb_trees = compile_trees("ftb6_2.mrg")
	grammar = PCFG()
	print("Extraction de la grammaire")
	grammar.extract_grammar(ftb_trees)
	print(grammar.regles["S"])

	print("Importation du lexique")
	lexique = defaultdict(str) 	# mot : cat (ne garde que la catégorie la plus probable)
	lexiquep = defaultdict(float)
	for cat in grammar.regles_lex:
		for mot in cat:
			if mot in lexique:
	    			if lexiquep[mot] < grammar.regles_lex[cat][mot]:
	    				lexique[mot] = cat
	    				lexiquep[mot] =  grammar.regles_lex[cat][mot]
			else:
				lexique[mot] = cat
				lexiquep[mot] =  grammar.regles_lex[cat][mot]	

	print(lexique)
	print("TEST",lexique["ou"])
	print("Importation des phrases à parser")
	document = open("test.txt","r", encoding = "utf8")
	phrase=document.readline()
	while phrase:
		phrase = phrase.split(" ")
		parse(phrase,grammar.regles,lexique)