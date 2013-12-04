#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from re import split as resplit
from tree import *
from utils import *

class PCFG() :
    
    def __init__ (self) :
        self.non_term = set()
        self.term = set()
        self.regles = defaultdict(lambda : defaultdict(float))                  # LH : RH : proba
        self.regles_lex = defaultdict(lambda : defaultdict(float))           # cat : mot : proba
        self.axiom = None
        
    def makerule(self,tree):
        if len(tree.subtrees) == 1 and tree.subtrees[0].lexique :
            mot = tree.subtrees[0].word
            # Noeud parent d'un lexical
            self.regles_lex[tree.word][mot] += 1.
            self.term.add(tree.word)
        else:
            self.non_term.add(tree.word)
            RH = " ".join(son.word for son in tree.subtrees)
            self.regles[tree.word][RH] += 1.
            for son in tree.subtrees :
                self.makerule(son)
        
    def extract_grammar(self,forest):
        def probabilise_counts(dico):
            for lev1 in dico:
                occ = sum(dico[lev1][lev2] for lev2 in dico[lev1])
                for lev2 in dico[lev1]:
                    dico[lev1][lev2] /= occ
        
        self.axiom = forest[0].label
        for tree in forest:
            assert tree.label == self.axiom
            self.makerule(tree)

        # mot: cat : compte
        lex_train = defaultdict(lambda : defaultdict(float))
        for cat in self.regles_lex :
            for word in self.regles_lex[cat] :
                lex_train[word][cat] = self.regles_lex[cat][word]
                
        # s'occuper du lexique
        self.add_external_lexicon({"lefff_5000.ftb4tags" : "utf8","lexique_cmpnd_TP.txt" : "latin1"},lex_train)
        
        probabilise_counts(self.regles)
        probabilise_counts(self.regles_lex)
        
    def add_external_lexicon(self,lexiques,lex_train):
        for lexique in lexiques:
            instream = open(lexique,"r",encoding=lexiques[lexique])
            for line in instream:
                if not line.isspace():
                    items = line.split("\t")
                    word,cat = items[0:2]
                    word.replace(" ","_")
                    if (word in lex_train and cat not in lex_train[word]) or not word in lex_train:
                        self.regles_lex[cat][word] = 1
                    
    def _export(self, dico, form_str, outname) :
        outstream = open(outname, "w", encoding = "utf8")
        for level1 in sorted(dico, key = lambda x : x != self.axiom) :
            for level2 in dico[level1] :
                outstream.write(form_str(level1, level2, dico[level1][level2]))
        return outstream
        
    
    def export_grammar(self, filename = "ftb.bnf") :
        form_str = lambda x,y,z : "<" + x + "> = <" + y.replace(" ", "> <") + "> ; " + str(z) + "\n"
        # <SENT> = <NP> <PONCT> <VPinf> <PONCT> <VN> <PP> <NP> <PONCT> ; 0.00025239777889954568
        outstream = self._export(self.regles, form_str, filename)
        term_str = lambda x : "<" + x + "> = \"" + x.lower() +"\" ; 1.0\n"
        for term in self.term :
            outstream.write(term_str(term))
        outstream.close()

    def export_lexicon(self, filename = "ftb.lex") :
        # "qui"	'prowh'	0.08064516129032257841
        #form_str = lambda y, x, z : '"' + x + """"\t'""" + y.lower() + "'\t" +str(z) + '\n'
        form_str = lambda y, x, z : '"' + x + """"\t'""" + y.lower() + "'\n"
        self._export(self.regles_lex, form_str, filename).close()

    def binarise(self):
        for head in self.regles.copy().keys():
            for rule in self.regles[head].copy().keys():
                if len(rule.split( )) == 1 and rule not in self.term:

                    #Ajoute une rêgle non terminale A:B
                    new_rule = ":".join([head,rule])
                    p1 = self.regles[head][rule]

                    #Retire la règle originelle
                    del self.regles[head][rule]

                    #Modifie la grammaire
                    for temp_left in self.regles:
                        #Pour toute production de A
                        if temp_left == head:
                            #Augmente la probabilité pour compenser la supression de A -> B
                            for temp_right in self.regles[temp_left]:
                                self.regles[temp_left][temp_right] /= (1- p1)
                            continue
                    
                    for temp_left in self.regles.copy().keys():
                        #Pour toute production de B
                        if temp_left == rule:
                            for temp_right in self.regles[temp_left]:
                                if head in temp_right: print("erreur, ",head,"est réécris par ",rule)
                                #Assigne à la nouvelle rêgle les mêmes rêgles de réécriture et les mêmes probabilités que celles de B
                                self.regles[new_rule][temp_right]=self.regles[temp_left][temp_right]

                    for temp_left in self.regles:
                        print("Je suis ici !")
                        #Pour toutes les autres rêgles de productions C
                        for temp_right in self.regles[temp_left].copy().keys():
                            #Qui contiennent la rêgle A dans leur réécriture.C -x A y
                            if head in temp_right.split( ):
                                #Crée une nouvelle rêgle se réécrivant C -> x A:B y
                                self.regles[temp_left][" ".join([new_rule if x==head else x for x in temp_right.split( )])] = p1 * self.regles[temp_left][temp_right]
                                #Modifie les probabilités des rêgles contenant A pour en retirer la possibilité de A -> B
                                self.regles[temp_left][temp_right] *= (1-p1)

        for head in self.regles.copy().keys():
            for rule in self.regles[head].keys():
                if len(rule.split( )) > 2:
                    A = rule.split( )
                    B = A.pop(len(A)-1)
                    nouveau = "-".join(A)
                    self.regles[head][" ".join([nouveau,B])] = self.regles[head].pop(rule)
                    while len(A) > 1:
                        B = A.pop(len(A)-1)
                        nouveau2 = "-".join(A)
                        self.regles[nouveau] = { " ".join([nouveau2,B]): 1 }
                        nouveau = nouveau2



if __name__ == "__main__" :
    
    #test = "( (SENT (VN (CLS Nous) (V prions)) (NP (DET les) (NC cinéastes) (COORD (CC et) (NP (ADJ tous) (DET nos) (NC lecteurs)))) (PP (P de) (VPinf (ADV bien) (VN (VINF vouloir)) (VPinf (VN (CLO nous) (CLO en) (VINF excuser))))) (PONCT .)))"
    #result = extract(test)
    #print ("result == test?",str(result)==test)
    #print(test)
    #print(result)
    
    ftb_trees = compile_trees("ftb6_2.mrg")
    grammar = PCFG()
    grammar.extract_grammar(ftb_trees)
    grammar.export_lexicon()
    grammar.export_grammar()
    #grammar.binarise()
    #grammar.export_grammar(filename = "ftb_grammar_binarized.txt")
        

    result_trees = compile_trees("result.txt")
    for tree in result_trees:
        debinarise(tree)

    # result_trees = [ arbres dans l'ordre du fichier result.txt]
    # for tree in result_trees:
    #       faire un traitement
    # Arbre:
    #       noeud axiome
                #self.parent = None
                #self.axiome = True
                #self.label = texte: NP, "pierre"
                #self.lexique = False
                #self.subtrees = [ FILS ]
    # si le label contient "-", faire des machins
    # NOTE: les arbres sont des structures chaînées
    # Si tu fais:
    # fluxout = open(...)
    # for tree in result_trees
    #   fluxout.write(str(tree)+\n)
