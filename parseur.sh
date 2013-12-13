#!/bin/bash
# Script principal
# Lance un parseur ftb.lex.out situé dans sxpcfg sur un input donné en argument.
#
# Argument :
# 1: chemin vers sxpcfg
# 2: input
#
# Fichiers devant être présents:
#   main.py
#   extraction.py
#   utils.py
#   tree.py
#   parseur.sh (vous êtes ici)
#   une installation de SYNTAX

cp $2 $1
cd $1
./ftb.lex.out -n 1 -pnt "$2" > output_groupe5.txt
cd -
cp "$1output_groupe5.txt" ./
