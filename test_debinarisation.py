#!/usr/bin/env python
# -*- coding: utf-8 -*-

from extraction import *

phrase = "( (S (NP:N:Prout Pierre) (VP:V mange)))"
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
