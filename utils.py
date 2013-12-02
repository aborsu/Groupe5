#!/usr/bin/env python
# -*- coding: utf-8 -*-

from re import split as resplit

NUMS = set(("un","deux","trois","quatre","cinq","six","sept","huit","neuf",
        "dix","onze","douze","treize","quatorze","quinze","seize",
        "vingt","trente","quarante","cinquante","soixante",
        "cent","mille","millions","milliards","billions"))
EXCEPT_NUM = set(("un",))


def isnumword(word):
    splitted_words = resplit('[ \-_]',word)
    if len(splitted_words) == 1 and splitted_words[0] in EXCEPT_NUM:
        return False
    for word in splitted_words:
        if word not in NUMS:
            return False
    return True
