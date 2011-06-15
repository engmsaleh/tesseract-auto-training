#!/usr/bin/env python
#-*- coding:utf8 -*-

import os
import string
import shutil
import glob
import time
    
def weedout(img_file_name,image_folder):  
    """ Move the corresponding erroneous image/box-file pair to a faulty directory"""
    if(os.path.exists("failure")):
        #os.rmdir("failure")
        #os.mkdir("failure")
        pass
    else:
        os.mkdir("failure")
    
    image=image_folder+img_file_name+'.tif'
    boxfile=image_folder+img_file_name+'.box'
    
    
    shutil.move(image,"failure/")
    shutil.move(boxfile,"failure/")
    
    print "moved",img_file_name


def move_file(lang, filename):
    """move filename to lang dir with lang prefix"""
    time.sleep(.09) # It is needed for windows - otherwise files are not removed...
    target = lang + ".training_data/" + lang + "." + filename
    
    if os.path.exists(target):
        os.remove(target)
    if os.path.exists("./" + filename):
        print "Moving '%s' to '%s'" % (filename, target)
        os.rename("./" + filename, target)


def train(lang, filename):
    """Generates normproto, inttemp, Microfeat, unicharset and pffmtable"""
    output_dir = lang + "." + "training_data"
    dir = lang + "." + "images" + "/"
    
    if(os.path.exists(output_dir)):
        pass
    else:
        os.mkdir(output_dir)
   # os.chdir(output_dir)
    print "in train"
    image = filename + '.tif'
    box = filename + '.box'
    exec_string1='tesseract ' + dir + image + ' ' + filename + ' nobatch box.train.stderr'
    print exec_string1
    qpipe = os.popen4(exec_string1) # This returns a list.  The second list element is a file object from which you can read the command output.
    # this creates files: slk.Arial.exp15.tr, slk.Arial.exp15.txt
    o=qpipe[1].readlines() 
    pos=str(o).find('FAILURE') #Look for the word "FAILURE" in tesseract-ocr trainer output.
    #print str(o)

    # Compute the Character Set
    exec_string2="unicharset_extractor"
    for name in glob.glob(dir + '/*.box'):
        exec_string2 += " " + name  
    qpipe4 = os.popen4(exec_string2)
    # this creates files: unicharset
    print exec_string2

    # TODO: font_properties (new in 3.01)
    
    # Clustering  
    tr_string = ""
    for tr_file in glob.glob('*.tr'):
        tr_string += tr_string + " " + tr_file

    #exec_string3="mftraining -F font_properties -U unicharset"
    exec_string3="mftraining -U unicharset " + tr_string
    exec_string4="cntraining " + tr_string

    print exec_string3
    qpipe2=os.popen4(exec_string3)
    # this creates files: inttemp, mfunicharset, pffmtable, Microfeat
    print exec_string4
    qpipe3=os.popen4(exec_string4)
    # this creates files: normproto

    #Now rename the 5 training files so it can be readily used with tesseract
    move_file(lang, "unicharset")
    move_file(lang, "inttemp")
    move_file(lang, "mfunicharset")
    move_file(lang, "pffmtable")
    move_file(lang, "Microfeat")
    move_file(lang, "normproto")

    #Putting it all together
    exec_string5= "combine_tessdata " + lang + ".training_data/" + lang +"."
    print exec_string5
    qpipe3=os.popen4(exec_string5)

    # TODO: dictionary
 
    # Cleaning...
    os.remove(filename + ".txt")
    os.remove(filename + ".tr")
