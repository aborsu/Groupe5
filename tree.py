#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from re import split as resplit
from utils import *


class Tree() :
    def __init__(self,name,lex) :
        self.parent = None
        self.axiome = False
        self.label = name
        self.word = name
        self.lexique = lex
        self.subtrees = []
        
    def __str__(self):
        if self.lexique :
            pre = " "+self.label
            post = ""
        else:
            if self.axiome:
                pre = "( ("+self.label
                post = "))"
            else:
                pre = " ("+self.label
                post = ")"
        sons = "".join([str(node) for node in self.subtrees])
        stringtree = pre + sons + post
        return stringtree

def compile_trees(filename) :
    instream = open(filename, "r", encoding = "utf8")
    phrase = instream.readline()
    ftb_trees = []
    
    while phrase :
        phrase = phrase.strip("\n")
        if phrase:
            ftb_trees.append(extract(phrase))
            phrase = instream.readline()
    return ftb_trees

def extract(phrase) :
    #( (SENT (VN (CLS Nous) (V prions)) (NP (DET les) (NC cinéastes) (COORD (CC et) (NP (ADJ tous) (DET nos) (NC lecteurs)))) (PP (P de) (VPinf (ADV bien) (VN (VINF vouloir)) (VPinf (VN (CLO nous) (CLO en) (VINF excuser))))) (PONCT .)))
    # (SENT (NP les_etudiants))

    # ( : nouveau noeud étiquette SENT. EMPILE "(". parent = SENT
    # ( : nouveau noeud etiquette NP. parent.ajouter_fils : NP. EMPILE "(". parent = NP
    # espace les_etudiants: nouveau noeud les_etudiants. parent.ajouter_fils : les_etudiants
    # ) : depiler
    # ) : dépiler
    
    # Au debut, garder un pointeur sur l'axiome.
    # - split sur espaces
    # Si début = parenthèse, alors l'empiler (strip)
    # tant que fin = parenthèse, dépiler (-1)
    # S'il reste des chars, alors : nouveau noeud (lexique?), 
    #   le noeud parent a pour fils ce nouveau noeud. 
    #   Le nouveau noeud devient parent.
    
    traitable = phrase.split(" ")
    axiome = None
    pile = []
    first_lexical = True
    
    for item in traitable:
        label = item.strip("()")
        node = None
        lexical = len(item)>0 and item[0] != "("
        if len(label) > 0:
            node = Tree(label,lexical)
            if not axiome:
                axiome = node
                parent = None
                node.axiome = True
            else:
                parent = pile[-1]
                # ===========  Normalisation du label/word  ==================
                # On demajuscule les premiers mots de phrase non entites nommées du ftb.
                if first_lexical and lexical and parent != "NPP":
                    first_lexical = False
                    node.word = label[0].lower()+label[1:]
                # On ajoute _NUM pour toutes les categories pertinentes
                if isnumber(label) or isnumword(label) :
                    TAGGED_WORDS["_NUM"].append(parent.word)
            node.parent = parent
            if parent:
                parent.subtrees.append(node)
        if len(item) > 0 and item[0] == "(":
            pile.append(node)
            item = item[1:]
        assert len(item) == 0 or item[0] != "(", "NOEUD SANS LABEL !"
        while  len(item) > 0 and item[-1] == ")":
            pile.pop()
            item = item[:-1]
    
    
    #print("|",phrase,"|",axiome,"|",sep="")
    assert  len(pile) == 0, "STRUCTURE MAL FORMEE !"
    assert str(axiome)==phrase, "ECHEC DE L'ANALYSE !"
    return axiome


def debinarise(maintree):
    """
    Prend une phrase sous forme d'arbre binaire et applatit l'arbre (arbre n-aire).
    """

    def _get_subtrees(tree,x):
        """
        Permet d'obtenir l'ensemble des noeuds qu'il faut applatir lorsqu'un noeud combiné est détecté.
        tree est le noeud dans lequel il faut aller chercher les sous-noeuds à applatir.
        x = nombre de noeuds qui ont été combinés.
        """
        list_of_subtrees = []
        liste = tree.subtrees #Liste des sous noeuds du noeud (Toujours 2 puisque l'arbre est binaire.)
        list_of_subtrees.append(liste[1]) #Le deuxième noeud est récupéré et envoyé dans la liste de réponse
        #list_of_subtrees[x] = liste[1]
        if x>2:
            rest = _get_subtrees(liste[0],x-1)      #S'il reste plus de deux noeuds à récupérer, on regarde à l'intérieur du premier noeud pour 1 noeud de moins.
            list_of_subtrees.extend(rest)
        else:
            list_of_subtrees.append(liste[0])
        return list_of_subtrees
    
    #pour chaque 
    #print(maintree.subtrees)
    for tree in maintree.subtrees:
        #print("test",tree.label)
        if "-" in tree.label:
           # print("ici")
            #Si on trouve un noeud composé
            ## Initialiser la liste à la bonne longueur (len(tree.label.split("-")))
            # x = len(tree.label.split("-"))
            # list_of_subtrees = [None] * x
            list_of_subtrees = _get_subtrees(tree,len(tree.label.split("-")))   #Remplis la liste de sous-noeuds d'autants de noeuds qu'il y a de labels dans le noeud composé.
            premier = list_of_subtrees.pop()
            premier.parent = maintree
            #ATTENTION Ceci ne fonctionne que si l'on a respecté le principe que les rêgles se binarise en agglutinant les éléments à gauches.
            #print("problème")
            #print(maintree.subtrees)
            #print(premier)
            maintree.subtrees[0] = premier
            i=1 
            while len(list_of_subtrees) > 0:
                new_tree = list_of_subtrees.pop()
                new_tree.parent = maintree 
                maintree.subtrees.insert(i,new_tree)   #On insère le noeud à la place
                i+=1

    for i,tree in enumerate(maintree.subtrees):
        if ":" in tree.label:
            liste = tree.label.split(":")   #Split le noeud
            
            parent = tree.parent                    #initialise la valeur parent
            new_tree = Tree(liste.pop(0),False)     #crée un nouveau noeud avec comme nom le premier élément de la liste et enlève l'élément de la liste.
            
            while len(liste)>0:                     #Tant qu'il reste des élément dans la liste (SI le noeud en combine plus de deux)
                new_tree.parent = parent            #Assigne à un noeud son parent
                if parent == tree.parent:
                    parent.subtrees[i] = new_tree   #S'il s'agit du premier noeud, modifie le noeud 'tree' pour qu'il pointe mainenant vers le nouveau noeud mais garde l'ordre
                else:
                    parent.subtrees = [new_tree]    #S'il ne s'agit pas du premier noeud créé, alors le nouveau noeud est le seur fils de son parent.
                
                parent = new_tree                   #Le nouveau noeud sera le parent du suivant
                new_tree = Tree(liste.pop(0),False) #Crée le noeud suivant dans la liste et l'enlève du même coup.
            
            new_tree.parent = parent                #Si la liste est vide, le parent est le noeud précédent.
            new_tree.subtrees = tree.subtrees       #
            parent.subtrees = [new_tree]
            
    
    #Récursivité
    if maintree.subtrees == []:
        return
    for subtree in maintree.subtrees:
        debinarise(subtree)
