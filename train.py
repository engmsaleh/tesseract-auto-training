#!/usr/bin/env python
#-*- coding:utf8 -*-
"""
This is python module for tesseract training process
"""

import os
import re
import shutil
import glob
import time
import subprocess

from datetime import datetime

def find_tesseract():
    """Find best version of tesseract"""
    # TODO
    highest_version = 'tesseract '
    return highest_version

def put_font_info(lang, search_font):
    """Put font info to font_properties file"""
    inputfile = lang + ".training_data/" + lang + ".font_properties"

    if os.path.exists(inputfile):
        newlines = []
        font_found = False
        fileconfig = open(inputfile, "r")
        for line in fileconfig:
            # find exact match
            matchObj = re.match( r'^%s ' %(search_font), line, re.M)
            if matchObj:
                font_found = True
            if line.strip():
                newlines.append(line)

        # TODO: get font info
        
        if font_found == False:
            newlines.append("%s 0 0 0 0 0\n" % search_font)
            file_out = open(inputfile, "w")
            for line in newlines:
                file_out.write(line)
            file_out.write('\n')
            file_out.close()
            print "WARNING: Font entry for '%s' was added to file '%s' " + \ 
                "with inicial data. Do not forget to review it!!!" \
                % (search_font, inputfile)
    else:
        file_o = open(inputfile, "w")
        file_o.write("#%s <fontname> <italic> <bold> <fixed> <serif> " + \
            "<fraktur>\n")
        file_o.write("timesitalic 1 0 0 1 0\n")
        file_o.write("%s 0 0 0 0 0\n\n" % search_font)
        file_o.close()
        print "WARNING: There was created file '%s' with inicial font  " + \
            "entry. Do not forget to review it!!!" % (inputfile)

def put_version_info(lang, work_dir):
    """Put version info to config file"""
    inputfile = work_dir + lang + ".config"
    if os.path.exists(inputfile):
        newlines = []
        version_info = False
        fileconfig = open(inputfile, "r")
        for line in fileconfig:
            if '# VERSION:' in line:
                newlines.append("# VERSION: %s\n" % str(datetime.today()))
                version_info = True
            else:
                newlines.append(line)

        if version_info == False:
            newlines = "# VERSION: %s\n" % str(datetime.today()) + newlines

        file_out = open(inputfile, "w")
        for line in newlines:
            file_out.write(line)
        file_out.close()
    else:
        file_o = open(inputfile, "w")
        file_o.write("# VERSION: " + str(datetime.today()))
        file_o.close()

def weedout(img_file_name, image_folder):
    """Move the corresponding erroneous image/box-file pair
        to a faulty directory"""
    if(os.path.exists("failure")):
        #os.rmdir("failure")
        #os.mkdir("failure")
        pass
    else:
        os.mkdir("failure")

    image = image_folder + img_file_name + '.tif'
    boxfile = image_folder + img_file_name + '.box'

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

    put_font_info(lang, filename.split('.')[1])
    
    # Clustering
    tr_string = ""
    for tr_file in glob.glob('*.tr'):
        tr_string += tr_string + " " + tr_file

    exec_string3 = "mftraining -F %s -U unicharset" % (lang + ".training_data/" + lang + ".font_properties")
    #exec_string3 = "mftraining -U unicharset " + tr_string
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
    put_version_info(lang, lang + ".training_data/")
    
    # Putting it all together
    exec_string5 = "combine_tessdata " + lang + ".training_data/" + lang + "."
    print "Running: ", exec_string5
    output5 = subprocess.Popen(exec_string5, stdout=subprocess.PIPE, \
                             stderr=subprocess.STDOUT, \
                             shell=True).communicate()[0]
    print output5

    # Cleaning...
    if os.path.exists(filename + ".txt"):
        os.remove(filename + ".txt")
    if os.path.exists(filename + ".tr"):
        os.remove(filename + ".tr")


def main():
    """Main"""
    #TODO: implement command line traning
    #train(lang, filename)


if __name__ == '__main__':
    main()
