#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict

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

class PCFG() :
    
    def __init__ (self) :
        self.non_term = set()
        self.regles = defaultdict(lambda : defaultdict(float))                  # LH : RH : proba
        self.lexique_train = defaultdict(lambda : defaultdict(float))           # mot : cat : proba
        #self.lexique_externe = { }  # mot : cat
        #self.lexique_test = { }     # mot : cat
        
    def makerule(self,tree):
        if len(tree.subtrees) == 1 and tree.subtrees[0].lexique :
            mot = tree.subtrees[0].word
            # Noeud parent d'un lexical
            self.lexique_train[mot][tree.word] += 1.
        else:
            RH = " ".join(son.word for son in tree.subtrees)
            self.regles[tree.word][RH] += 1.
            for son in tree.subtrees :
                self.makerule(son)
        
    def extract_grammar(self,forest):
        for tree in forest:
            self.makerule(tree)
        
        for LHS in self.regles :
            occ = sum(self.regles[LHS][RHS] for RHS in self.regles[LHS])
            for RHS in self.regles[LHS] :
                self.regles[LHS][RHS] /= occ
        
        lst = []
        for LH in self.regles :
            for RH in self.regles[LH] :
                lst.append(self.regles[LH][RH])
        
        lst.sort()
        print(sum(lst) / len(lst))
        print(lst[:30])
        
        #print(self.regles["VN"]["CLO VINF"])

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
                # On demajuscule les premiers mots de phrase non entites nommées du ftb.
                if first_lexical and lexical and parent != "NPP":
                    first_lexical = False
                    node.word = label[0].lower()+label[1:]
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
            
    
def compile_trees(filename) :
    instream = open("ftb6_2.mrg", "r", encoding = "utf8")
    phrase = instream.readline()
    ftb_trees = []
    
    while phrase :
        phrase = phrase.strip("\n")
        if phrase:
            ftb_trees.append(extract(phrase))
            phrase = instream.readline()
    return ftb_trees


if __name__ == "__main__" :
    
    #test = "( (SENT (VN (CLS Nous) (V prions)) (NP (DET les) (NC cinéastes) (COORD (CC et) (NP (ADJ tous) (DET nos) (NC lecteurs)))) (PP (P de) (VPinf (ADV bien) (VN (VINF vouloir)) (VPinf (VN (CLO nous) (CLO en) (VINF excuser))))) (PONCT .)))"
    #result = extract(test)
    #print ("result == test?",str(result)==test)
    #print(test)
    #print(result)
    
    ftb_trees = compile_trees("ftb6_2.mrg")
    grammar = PCFG()
    grammar.extract_grammar(ftb_trees)
    #print("\n".join(str(x) for x in ftb_trees[:6]))
        
