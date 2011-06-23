#!/usr/bin/env python
#-*- coding:utf8 -*-
""" Correct None script in unicharset to real script name """

import sys
import codecs

def find_script_name(u_c):
    """ Find correct script based on table replacement.
        Replacement dictionary was created based on tesseract 
        traineddata files
    """
    return {
         'ثم' : 'Arabic',
        'NULL' : 'Common',
        '0' : 'Common',
        '1' : 'Common',
        '2' : 'Common',
        '3' : 'Common',
        '4' : 'Common',
        '5' : 'Common',
        '6' : 'Common',
        '7' : 'Common',
        '8' : 'Common',
        '9' : 'Common',
        "'" : 'Common',
        '"' : 'Common',
        '-' : 'Common',
        '!' : 'Common',
        '#' : 'Common',
        '$' : 'Common',
        '%' : 'Common',
        '&' : 'Common',
        '(' : 'Common',
        ')' : 'Common',
        '*' : 'Common',
        ',' : 'Common',
        '.' : 'Common',
        '/' : 'Common',
        ':' : 'Common',
        ';' : 'Common',
        '?' : 'Common',
        '@' : 'Common',
        '[' : 'Common',
        '\\' : 'Common',
        ']' : 'Common',
        '^' : 'Common',
        '_' : 'Common',
        '`' : 'Common',
        '{' : 'Common',
        '|' : 'Common',
        '}' : 'Common',
        '~' : 'Common',
        '”' : 'Common',
        '‹' : 'Common',
        '›' : 'Common',
        '+' : 'Common',
        '<' : 'Common',
        '=' : 'Common',
        '>' : 'Common',
        '±' : 'Common',
        '«' : 'Common',
        '»' : 'Common',
        '©' : 'Common',
        '†' : 'Common',
        '€' : 'Common', ##
        '„' : 'Common', ##
        '…' : 'Common', ##
        '‘' : 'Common', ##
        '’' : 'Common', ##
        '“' : 'Common', ##
        '•' : 'Common', ##
        '—' : 'Common', ##
        '™' : 'Common', ##
        'ˇ' : 'Common', ##
        '˘' : 'Common', ##
        '§' : 'Common', ##
        '®' : 'Common', ##
        '°' : 'Common', ##
        '×' : 'Common', ##
        '÷' : 'Common', ##
        'a' : 'Latin',
        'A' : 'Latin',
        'á' : 'Latin',
        'Á' : 'Latin',
        'â' : 'Latin',
        'Ă' : 'Latin',
        'ă' : 'Latin',
        'ą' : 'Latin',
        'ä' : 'Latin',
        'Ä' : 'Latin',
        'b' : 'Latin',
        'B' : 'Latin',
        'c' : 'Latin',
        'C' : 'Latin',
        'ć' : 'Latin',
        'ç' : 'Latin',
        'č' : 'Latin',
        'Č' : 'Latin',
        'd' : 'Latin',
        'D' : 'Latin',
        'ď' : 'Latin',
        'Ď' : 'Latin',
        'e' : 'Latin',
        'E' : 'Latin',
        'é' : 'Latin',
        'É' : 'Latin',
        'ě' : 'Latin',
        'Ě' : 'Latin',
        'F' : 'Latin',
        'f' : 'Latin',
        'G' : 'Latin',
        'g' : 'Latin',
        'h' : 'Latin',
        'H' : 'Latin',
        'i' : 'Latin',
        'I' : 'Latin',
        'Í' : 'Latin',
        'í' : 'Latin',
        'j' : 'Latin',
        'J' : 'Latin',
        'k' : 'Latin',
        'K' : 'Latin',
        'l' : 'Latin',
        'L' : 'Latin',
        'ĺ' : 'Latin',
        'Ľ' : 'Latin',
        'ľ' : 'Latin',
        'ł' : 'Latin',
        'm' : 'Latin',
        'M' : 'Latin',
        'n' : 'Latin',
        'N' : 'Latin',
        'Ň' : 'Latin',
        'ň' : 'Latin',
        'o' : 'Latin',
        'O' : 'Latin',
        'ö' : 'Latin',
        'Ö' : 'Latin',
        'Ó' : 'Latin',
        'ó' : 'Latin',
        'ő' : 'Latin',
        'Ô' : 'Latin',
        'ô' : 'Latin',
        'p' : 'Latin',
        'P' : 'Latin',
        'q' : 'Latin',
        'Q' : 'Latin',
        'r' : 'Latin',
        'R' : 'Latin',
        'ŕ' : 'Latin',
        'ř' : 'Latin',
        'Ř' : 'Latin',
        's' : 'Latin',
        'S' : 'Latin',
        'ß' : 'Latin',
        'Š' : 'Latin',
        'š' : 'Latin',
        't' : 'Latin',
        'T' : 'Latin',
        'ť' : 'Latin',
        'Ť' : 'Latin',
        'u' : 'Latin',
        'U' : 'Latin',
        'ü' : 'Latin',
        'Ü' : 'Latin',
        'ú' : 'Latin',
        'Ú' : 'Latin',
        'ů' : 'Latin',
        'Ů' : 'Latin',
        'v' : 'Latin',
        'V' : 'Latin',
        'W' : 'Latin',
        'w' : 'Latin',
        'X' : 'Latin',
        'x' : 'Latin',
        'y' : 'Latin',
        'Y' : 'Latin',
        'ý' : 'Latin',
        'Ý' : 'Latin',
        'z' : 'Latin',
        'Z' : 'Latin',
        'ż' : 'Latin',
        'ž' : 'Latin',
        'Ž' : 'Latin',
        'Я' : 'Cyrillic',
        'к' : 'Cyrillic',
        'у' : 'Cyrillic',
        'й' : 'Cyrillic',
        'ж' : 'Cyrillic',
        'Ш' : 'Cyrillic',
        'µ' : 'Greek',
        'אָ' : 'Hebrew'
    }[u_c]

def correct_unicharset(inputfile):
    """ Open unicharset data file and correct script name"""
    filein = codecs.open(inputfile, encoding='utf-8')
    newlines = []
    unknown = ""
    for line in filein:
        data = line.strip().split(' ')
        if (len(data) == 4):  # 3.00 version
            if (data[2] == "NULL"):
                try:
                    script_name = find_script_name(data[0])
                    newlines.append("%s %s %s %s\n" % (data[0], data[1], \
                                    script_name, data[3]))
                except KeyError:
                    # print u"%s is not in the list." % (sys.exc_value)
                    newlines.append(line)
        else:
            newlines.append(line)
    filein.close()

    file_o = codecs.open(inputfile, encoding='utf-8', mode='w+')
    for line in newlines:
        file_o.write(line)
    file_o.write(unknown)
    file_o.close()
