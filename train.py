#!/usr/bin/env python
#-*- coding:utf8 -*-
"""
This is python module for tesseract training process
"""

import os
import shutil
import glob
import time
import subprocess

def find_tesseract():
    """Find best version of tesseract"""
    # TODO
    highest_version = 'tesseract '
    return highest_version


def weedout(img_file_name, image_folder):
    """Move the corresponding erroneous image/box-file pair
        to a faulty directory"""
    if(os.path.exists("failure")):
        #os.rmdir("failure")
        #os.mkdir("failure")
        pass
    else:
        os.mkdir("failure")

    image = image_folder+img_file_name+'.tif'
    boxfile = image_folder+img_file_name+'.box'


    shutil.move(image, "failure/")
    shutil.move(boxfile, "failure/")

    print "moved", img_file_name


def move_file(lang, filename):
    """Move filename to lang dir with lang prefix"""
    time.sleep(.09)
    # It is needed for windows - otherwise files are not removed...
    
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
    input_dir = lang + "." + "images" + "/"

    if(os.path.exists(output_dir)):
        pass
    else:
        os.mkdir(output_dir)
   # os.chdir(output_dir)
    print "in train"
    image = filename + '.tif'

    tesseract_cmd = find_tesseract()
    exec_string1 = tesseract_cmd + input_dir + image + ' ' + filename + \
                    ' nobatch box.train.stderr'

    print "Running: ", exec_string1
    output = subprocess.Popen(exec_string1, stdout=subprocess.PIPE, \
                             stderr=subprocess.STDOUT, \
                             shell=True).communicate()[0]
    # Print errors
    errors_string = "\nErrors:"
    output_lines = output.split('\n')
    for line in output_lines:
        if 'FAILURE' in line:
            errors_string = errors_string + '\n' + line

    if errors_string != "\nErrors:":
        errors_string += "\n"
        print errors_string

    # Compute the Character Set
    exec_string2 = "unicharset_extractor"
    for name in glob.glob(input_dir + '/*.box'):
        exec_string2 += " " + name

    print "Running: ",  exec_string2
    output2 = subprocess.Popen(exec_string2, stdout=subprocess.PIPE, \
                             stderr=subprocess.STDOUT, \
                             shell=True).communicate()[0]
    # this creates files: unicharset
    print output2

    # TODO: font_properties (new in 3.01)

    # Clustering
    tr_string = ""
    for tr_file in glob.glob('*.tr'):
        tr_string += tr_string + " " + tr_file

    #exec_string3="mftraining -F font_properties -U unicharset"
    exec_string3 = "mftraining -U unicharset " + tr_string
    exec_string4 = "cntraining " + tr_string

    print "Running3: ", exec_string3
    output3 = subprocess.Popen(exec_string3, stdout=subprocess.PIPE, \
                             stderr=subprocess.STDOUT, \
                             shell=True).communicate()[0]
    # this creates files: inttemp, mfunicharset, pffmtable, Microfeat
    # TODO: there is on output on Windows with tesseract 3.00
    print output3

    print "Running: ", exec_string4
    output4 = subprocess.Popen(exec_string4, stdout=subprocess.PIPE, \
                             stderr=subprocess.STDOUT, \
                             shell=True).communicate()[0]
    # this creates files: normproto
    print output4

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
    exec_string5 = "combine_tessdata " + lang + ".training_data/" + lang +"."
    print "Running: ", exec_string5
    output5 = subprocess.Popen(exec_string5, stdout=subprocess.PIPE, \
                             stderr=subprocess.STDOUT, \
                             shell=True).communicate()[0]
    print output5

    # Cleaning...
#    if os.path.exists(filename + ".txt"):
#        os.remove(filename + ".txt")
#    if os.path.exists(filename + ".tr"):
#        os.remove(filename + ".tr")
