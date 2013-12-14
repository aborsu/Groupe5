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
            if RH != tree.word: # Corrige les productions erronnées du corpus type X -> X
                self.regles[tree.word][RH] += 1.
            for son in tree.subtrees :
                self.makerule(son)
        
    def extract_grammar(self,forest,lexiques):
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
        self.add_external_lexicon(lexiques,lex_train)
        self.add_named_entities()
        
        probabilise_counts(self.regles)
        probabilise_counts(self.regles_lex)
        
    def add_external_lexicon(self,lexiques,lex_train):
        for lexique in lexiques:
            instream = open(lexique,"r",encoding=lexiques[lexique])
            for line in instream:
                if not line.isspace():
                    items = line.split("\t")
                    word,cat = items[0:2]
                    if "__" in word:
                        word_manual_cat = word.split("__")
                        word = word_manual_cat[0]
                    word = word.replace("_-_","_").replace(" ","_")
                    if (word in lex_train and cat not in lex_train[word]) or not word in lex_train:
                        self.regles_lex[cat][word] = 1
                        
    def add_named_entities(self):
        for tag in TAGGED_WORDS:
            for cat in TAGGED_WORDS[tag]:
                self.regles_lex[cat][tag] = 1
        
    def _export(self, dico, form_str, outname) :
        outstream = open(outname, "w", encoding = "utf8")
        for level1 in sorted(dico, key = lambda x : x != self.axiom) :
            for level2 in dico[level1] :
                if level2 == "\"":
                    rhs = "\\\""
                else:
                    rhs = level2
                outstream.write(form_str(level1, rhs, dico[level1][level2]))
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

    def export_grammar_bin(self, filename = "ftb_bin.bnf") :
        form_str = lambda x,y,z : "<" + x + "> = <" + y.replace(" ", "> <") + "> ; " + str(z) + "\n"
        # <SENT> = <NP> <PONCT> <VPinf> <PONCT> <VN> <PP> <NP> <PONCT> ; 0.00025239777889954568
        outstream = self._export(self.regles, form_str, filename)
        term_str = lambda x : "<" + x + "> = \"" + x.lower() +"\" ; 1.0\n"
        for term in self.term :
            outstream.write(term_str(term))
        outstream.close()

    def _find_unary_rules(self):
        rules_to_be_replaced = []
        for head in self.regles:
            for rule in self.regles[head] :
                if len(rule.split(" ")) == 1 and rule not in self.term:
                    #Ajoute une rêgle non terminale A:B
                    new_rule = ":".join([head,rule])
                    p = self.regles[head][rule]
                    rules_to_be_replaced.append([new_rule,head,rule,p])
        return rules_to_be_replaced

    def _insert_new_combined_rule(self,mod,old_head,warning,p1):
        nouvelles_regles = defaultdict(lambda : defaultdict(float)) 
        for head in self.regles:
            for rule in self.regles[head]:
                bag = rule.split(" ")
                if old_head in bag:
                    p2 = self.regles[head][rule]
                    new_rule = " ".join([mod if x==old_head else x for x in bag])
                    nouvelles_regles[head][new_rule] = p1 * p2
                    self.regles[head][rule] = (1-p1) * p2
        return nouvelles_regles

    def _find_morethan2ary_rules(self):
        nouvelles_regles = defaultdict(lambda : defaultdict(float)) 
        rules_to_be_removed = []
        for h in self.regles:
            for r in self.regles[h] :
                if len(r.split( )) > 2:
                    rules_to_be_removed.append([h,r])
                    a = r.split( )
                    b = a.pop(len(a)-1)
                    nouveau = "-".join(a)
                    nouvelles_regles[h][" ".join([nouveau,b])] = self.regles[h][r]
                    while len(a) > 1:
                        b = a.pop(len(a)-1)
                        nouveau2 = "-".join(a)
                        nouvelles_regles[nouveau][" ".join([nouveau2,b])] = 1
                        nouveau = nouveau2
        return nouvelles_regles, rules_to_be_removed

    def update(self,dico2):
        for h in dico2:
            for r in dico2[h]:
                self.regles[h][r] = dico2[h][r]


    def binarise(self):        
        #1 Trouve toutes les rêgles unaires non terminales de la grammaire qui doivent être remplacée. 
        rtbr = self._find_unary_rules()

        #2 Enlêve les originaux
        for r in rtbr:
            del self.regles[r[1]][r[2]]

        #3 Crée des rêgles faisant appel à la nouvelle rêgle et met à jour le dictionnaire
        for rule in rtbr:
            nouvelles_regles = self._insert_new_combined_rule(rule[0],rule[1],rule[2],rule[3])
            self.update(nouvelles_regles)

        #4 Modifie les probabilités des rêgles ayant la même tête
        for rule in rtbr:
            for rule2 in self.regles[rule[1]]:
                self.regles[rule[1]][rule2] *=(1-rule[3])

        #5 Binarise les rêgles plus que 2aires
        nouvelles_regles, rtbr = self._find_morethan2ary_rules()
        self.update(nouvelles_regles)
        
