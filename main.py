#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from extraction import *

if __name__ == '__main__':
    from optparse import OptionParser

    ############# Traitement de la ligne de commande & options ################
    usage = """ Parsing probabiliste d'une chaîne pré-traitée.
                Ce programme :
                    - Extrait une grammaire probabilisée d'un corpus arboré au format Berkeley.
                    - L'enrichit avec des lexiques externes
                    - Binarise éventuellement la grammaire
                python3 %prog -t corpus_arbore -f corpus_input (-l lexique.txt encoding)* (-b) (-i|-c)
            """
    parser=OptionParser(usage=usage)
    parser.add_option("-t", "--train", action="store", type="string", dest="train", default="ftb6_2.mrg", help="Corpus arbore d'ou extraire la PCFG.")
    parser.add_option("-l", "--lexiques", action="append", type="string", nargs=2, dest="lexiques", help="Lexiques additionnels et leur encoding.")
    parser.add_option("-b", "--binariser", action="store_true", dest="binariser", help="Binariser la grammaire")

    (opts,args) = parser.parse_args()
    global TEST,INTERNE,COMMANDE
    if opts.lexiques and len(opts.lexiques) > 0 :
        lexiques = dict(opts.lexiques)
    else:
        lexiques = {"lefff_5000.ftb4tags" : "utf8","lexique_cmpnd_TP.txt" : "latin1"}

    ############# Extraction de la grammaire ##############
    print("Construction des arbres")
    ftb_trees = compile_trees(opts.train)
    grammar = PCFG()
    print("Extraction de la grammaire")
    grammar.extract_grammar(ftb_trees,lexiques)
    if opts.binariser : ## EN PANNE.
        print("Binarisation de la grammaire")
        grammar.binarise()
    print("Export de la grammaire")
    grammar.export_lexicon()
    grammar.export_grammar()

        

