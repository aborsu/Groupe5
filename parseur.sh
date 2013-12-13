#!/bin/bash
# Script principal
# Lance l'extraction de la grammaire et du corpus (main.py)
# Entraîne un parseur externe (SYNTAX) sur la grammaire et le lexique extrait
# Lance ledit parser sur un fichier pré-traité
#
# Argument : chemin vers spec
#
# Fichiers devant être présents:
#   main.py
#   extraction.py
#   utils.py
#   tree.py
#   parseur.sh (vous êtes ici)
#   une installation de SYNTAX

python3 main.py -t ftb6_2.mrg -l "lefff_5000.ftb4tags" "utf8" -l "lexique_cmpnd_TP.txt" "latin1"
cp ftb.lex $1
cp ftb.bnf $1
cd $1
make foo.lex.out 
?????? -n 1 -pnt -string
