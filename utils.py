#!/usr/bin/env python
# -*- coding: utf-8 -*-

from re import split as resplit


NUMS = set(("un","deux","trois","quatre","cinq","six","sept","huit","neuf",
        "dix","onze","douze","treize","quatorze","quinze","seize",
        "vingt","trente","quarante","cinquante","soixante",
        "cent","mille","millions","milliards","billions"))
EXCEPT_NUM = set(("un",))
TAGGED_WORDS = {"_QUOTE":["PONCT"],
                "_ORG":["NPP"],
                "_PERS":["NPP"],
                "_URL":["NPP"],
                "_GEO":["NPP"],
                "_DATE":["NPP","NC"], # Parfois un NP entier, parfois le + _date
                "_NUM":[] #complété selon train
                }

def isnumber(word):
    nums = word.split(",")
    for num in nums:
        if not word.isnumeric():
            return False
    return True
    
def isnumword(word):
    splitted_words = resplit('[ \-_]',word)
    if len(splitted_words) == 1 and splitted_words[0] in EXCEPT_NUM:
        return False
    for word in splitted_words:
        if word not in NUMS:
            return False
    return True

