#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Filename: create_multipage.py
    Description: create multipage tiff base on available box files

    Copyright (C) 2011 Zdenko Podobný
    Website: http://www.sk-spell.sk.cx/tesseract-ocr-en

    This program is released under the Apache License 2.0
"""

import glob
import sys
import os.path
from subprocess import Popen, PIPE, call

page = 0
finalBoxData = ""
convertString = ""
finaleBoxFile = "slk-frak.test.exp001.box"
finaleImageBoxFile = "slk-frak.test.exp001.tif"

print ("Processing files in current directory:\n")

boxFiles = glob.glob('*.box') 
try:
    boxFiles.remove(finaleBoxFile)
except:
    pass
finaleBox = open(finaleBoxFile, 'w')

for fname in boxFiles:
    # check if image exists
    rootName = fname.rsplit('.', 1)[0]
    for ext in ('.tif', '.png', '.bmp', '.jpg', '.jpeg'):
        imageExists = False
        if os.path.isfile(rootName + ext):
            print (rootName + ext)
            convertString = convertString + rootName + ext + " "
            imageExists = True
            break

    # if image exists than process its box file
    if (imageExists):
        print (fname + "\n")
        fileBox = open(fname, 'r')
        for line in fileBox:
            data = line.split(' ')
            for i in range(0,5):
                finaleBox.write(data[i] + " ")
            finaleBox.write(str(page) + "\n")
        fileBox.close()   
        page += 1

finaleBox.close()

print "Joining images..."
try:
    retcode = call("convert " + convertString + finaleImageBoxFile, shell=True)
    if retcode < 0:
        print >>sys.stderr, "Was terminated by signal", -retcode
    else:
        print >>sys.stderr, "Finished with returned", retcode
except OSError, e:
    print >>sys.stderr, "Execution failed:", e
