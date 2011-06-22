#!/usr/bin/env python
#-*- coding:utf8 -*-

""" This code reads alphabet characters from certain files and fills up
    an array so it can be used for generating test images.
    """

import os


def combine(frest, fc_cont, fpresv, fpostsv):
    """ Creates all possible combinations of consonant + vowel """
    all_comb = []

    for rest in frest:
        rest = rest.strip()
        all_comb.append(rest)

    for c_val in fc_cont:
        c_val = c_val.strip()  # Remove special characters
        c1_val = c_val + " "
        all_comb.append(c1_val)
        for prev in fpresv:  # Combine consonant+vowel sign
            txt = prev.rstrip() + c_val
            all_comb.append(txt)
        for postv in fpostsv:  # Combine vowel sign+consonant
            txt = c_val + postv.strip()
            txt = txt + " "
            all_comb.append(txt)
    return all_comb


def read_file(alphabet_dir):
    """ Reads input alphabet files from alphabet_dir """
    # File containing vowels
    if(os.path.exists(alphabet_dir + "consonants")):
        file_cc = open(alphabet_dir + "consonants", 'r')
        fc_content = file_cc.readlines()
        file_cc.close()
    else:
        fc_content = []

    # File containing semivowels of the form consonant_conjunct+semivowel
    if(os.path.exists(alphabet_dir + "pre_semivowels")):
        file_ps = open(alphabet_dir + "pre_semivowels", 'r')
        fpresv = file_ps.readlines()
        file_ps.close()
    else:
        fpresv = []

    # File containing semivowels of the form semivowel+consonant_conjunct
    if(os.path.exists(alphabet_dir + "post_semivowels")):
        file_psv = open(alphabet_dir + "post_semivowels", 'r')
        fpostsv = file_psv.readlines()
        file_psv.close()
    else:
        fpostsv = []

    # File containing everything else
    if(os.path.exists(alphabet_dir + "rest")):
        file_rest = open(alphabet_dir + "rest", 'r')
        frest = file_rest.readlines()
        file_rest.close()
    else:
        frest = []
    return combine(frest, fc_content, fpresv, fpostsv)
