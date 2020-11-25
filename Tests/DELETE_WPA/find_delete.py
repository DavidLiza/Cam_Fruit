#!/usr/bin/env python
#-*- coding: utf-8 -*-
_author_= "David Lizarazo"
_version_="1.0.0"

import os
import re
from subprocess import call


with open("file.txt") as supplicant:
    lines=supplicant.readlines()
    cont = 0 
    for word in lines:
        if "MAKI2" in word:
            break
        cont += 1
    supplicant.close()

cont = cont-1

for x in range(4):
    lines.pop(cont)
    
with open("file.txt" , "w") as supplicant:
    new_file_contents = "".join(lines)
    supplicant.write(new_file_contents)
    supplicant.close()

    # if any("MAKI2" in word for word in lines):
    #     print ("Yeey")

    #r = re.compile('|'.join([r'\b%s\b' % w for w in lines]), flags=re.I)
    #enc = lines.findall("MAKI2")
    #print (enc)
    

