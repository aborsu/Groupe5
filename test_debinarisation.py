#!/usr/bin/env python
# -*- coding: utf-8 -*-

from extraction import *

phrases = ["( (S (NP:N:Prout Pierre) (VP:V mange)))",
    "( (S (NP:N:Prout Pierre) (VP (V-NP-Adj (V-NP (V broute) (NP Marie)) (Adj adroite)) (Adv délicatement))))",
    "( (S (NP:N:Prout Pierre) (VP (V-NP-Adj:N (V-NP (V broute) (NP Marie)) (Adj:N adroite)) (Adv délicatement))))"]

for phrase in phrases:
    tree = extract(phrase)
    print(tree)
    print('Debinarise')
    debinarise(tree)
    print(tree)


# output:

# (S (NP Paul) (VP (V-NP (V mange) (NP (N léon))) (Adv lentement)))


# debinarisé :
# (S (NP Paul) (VP
#                 (V mange)
#                 (NP (N léon))
#                 (Adv lentement)
#             ))


# Defactoriser:
#     (PP-NP  ... )

#     (PP (NP ... ) )
