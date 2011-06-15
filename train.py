#!/usr/bin/env python
#-*- coding:utf8 -*-

import os
import string
import shutil
import glob
import time
import subprocess

def find_tesseract():
    """Find best version of tesseract"""
    # TODO
    highest_version = 'tesseract '
    return highest_version


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
    # TODO: check for errors e.g. no output files...
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

    tesseract_cmd = find_tesseract()
    exec_string1=tesseract_cmd + dir + image + ' ' + filename + ' nobatch box.train.stderr'
    print exec_string1

    qpipe1 = subprocess.Popen(exec_string1, shell=True, stdin=subprocess.PIPE, \
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # This creates files: slk.Arial.exp15.tr, slk.Arial.exp15.txt
    
    #Look for the word "FAILURE" in tesseract-ocr trainer output.
    #qpipe = os.popen4(exec_string1) 
    # This returns a list.  The second list element is a file object from which you can read the command output.
    #o=qpipe[1].readlines() 
    #pos=str(o).find('FAILURE')
    #print str(o)

    # Compute the Character Set
    exec_string2="unicharset_extractor"
    for name in glob.glob(dir + '/*.box'):
        exec_string2 += " " + name  
    qpipe2 = subprocess.Popen(exec_string2, shell=True, stdin=subprocess.PIPE, \
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
    qpipe3 = subprocess.Popen(exec_string3, shell=True, stdin=subprocess.PIPE, \
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # this creates files: inttemp, mfunicharset, pffmtable, Microfeat

    print exec_string4
    qpipe4 = subprocess.Popen(exec_string4, shell=True, stdin=subprocess.PIPE, \
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # this creates files: normproto

    # Now rename the 5 training files so it can be readily used with tesseract
    move_file(lang, "unicharset")
    move_file(lang, "inttemp")
    move_file(lang, "mfunicharset")
    move_file(lang, "pffmtable")
    move_file(lang, "Microfeat")
    move_file(lang, "normproto")

    # TODO: dictionary    
    # TODO: create lang.config with version info ;-)

    # Putting it all together
    exec_string5= "combine_tessdata " + lang + ".training_data/" + lang +"."
    print exec_string5
    qpipe5 = subprocess.Popen(exec_string5, shell=True, stdin=subprocess.PIPE, \
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
 
    # Cleaning...
    if os.path.exists(filename + ".txt"):
        os.remove(filename + ".txt")
    if os.path.exists(filename + ".tr"):
        os.remove(filename + ".tr")
