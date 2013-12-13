#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def decurlybracketify(filename = "ftb_test_accolades.txt") :
    instream = open(filename, "r",  encoding = "utf8")
    pattern1 = "{[^}]+}[^\s]+"
    pattern2 = "{[^}]+}"
    
    # liste de couples (liste de token, dictionnaire {token : token entre accolade})
    sentences = []
    
    for line in instream :
        parseTokToInitialTok = {}
        curlybracketed = re.findall(pattern1, line)
        for word in curlybracketed :
            pair = word.strip("{ \n").split("}")
            parseTokToInitialTok[pair[1]] = pair[0]
        
        parsable_sentence = re.sub(pattern2, "", line)
        sentences.append((parsable_sentence.split(), parseTokToInitialTok))
    
    instream.close()
    
    return sentences

main()
