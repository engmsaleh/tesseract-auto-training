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
        u'ثم' : 'Arabic',
        u'NULL' : 'Common',
        u'0' : 'Common',
        u'1' : 'Common',
        u'2' : 'Common',
        u'3' : 'Common',
        u'4' : 'Common',
        u'5' : 'Common',
        u'6' : 'Common',
        u'7' : 'Common',
        u'8' : 'Common',
        u'9' : 'Common',
        "'" : 'Common',
        u'"' : 'Common',
        u'-' : 'Common',
        u'!' : 'Common',
        u'#' : 'Common',
        u'$' : 'Common',
        u'%' : 'Common',
        u'&' : 'Common',
        u'(' : 'Common',
        u')' : 'Common',
        u'*' : 'Common',
        u',' : 'Common',
        u'.' : 'Common',
        u'/' : 'Common',
        u':' : 'Common',
        u';' : 'Common',
        u'?' : 'Common',
        u'@' : 'Common',
        u'[' : 'Common',
        u'\\' : 'Common',
        u']' : 'Common',
        u'^' : 'Common',
        u'_' : 'Common',
        u'`' : 'Common',
        u'{' : 'Common',
        u'|' : 'Common',
        u'}' : 'Common',
        u'~' : 'Common',
        u'”' : 'Common',
        u'‹' : 'Common',
        u'›' : 'Common',
        u'+' : 'Common',
        u'<' : 'Common',
        u'=' : 'Common',
        u'>' : 'Common',
        u'±' : 'Common',
        u'«' : 'Common',
        u'»' : 'Common',
        u'©' : 'Common',
        u'†' : 'Common',
        u'€' : 'Common', ##
        u'„' : 'Common', ##
        u'…' : 'Common', ##
        u'‘' : 'Common', ##
        u'’' : 'Common', ##
        u'“' : 'Common', ##
        u'•' : 'Common', ##
        u'—' : 'Common', ##
        u'™' : 'Common', ##
        u'ˇ' : 'Common', ##
        u'˘' : 'Common', ##
        u'§' : 'Common', ##
        u'®' : 'Common', ##
        u'°' : 'Common', ##
        u'×' : 'Common', ##
        u'÷' : 'Common', ##
        u'a' : 'Latin',
        u'A' : 'Latin',
        u'á' : 'Latin',
        u'Á' : 'Latin',
        u'â' : 'Latin',
        u'Ă' : 'Latin',
        u'ă' : 'Latin',
        u'ą' : 'Latin',
        u'ä' : 'Latin',
        u'Ä' : 'Latin',
        u'b' : 'Latin',
        u'B' : 'Latin',
        u'c' : 'Latin',
        u'C' : 'Latin',
        u'ć' : 'Latin',
        u'ç' : 'Latin',
        u'č' : 'Latin',
        u'Č' : 'Latin',
        u'd' : 'Latin',
        u'D' : 'Latin',
        u'ď' : 'Latin',
        u'Ď' : 'Latin',
        u'e' : 'Latin',
        u'E' : 'Latin',
        u'é' : 'Latin',
        u'É' : 'Latin',
        u'ě' : 'Latin',
        u'Ě' : 'Latin',
        u'F' : 'Latin',
        u'f' : 'Latin',
        u'G' : 'Latin',
        u'g' : 'Latin',
        u'h' : 'Latin',
        u'H' : 'Latin',
        u'i' : 'Latin',
        u'I' : 'Latin',
        u'Í' : 'Latin',
        u'í' : 'Latin',
        u'j' : 'Latin',
        u'J' : 'Latin',
        u'k' : 'Latin',
        u'K' : 'Latin',
        u'l' : 'Latin',
        u'L' : 'Latin',
        u'ĺ' : 'Latin',
        u'Ľ' : 'Latin',
        u'ľ' : 'Latin',
        u'ł' : 'Latin',
        u'm' : 'Latin',
        u'M' : 'Latin',
        u'n' : 'Latin',
        u'N' : 'Latin',
        u'Ň' : 'Latin',
        u'ň' : 'Latin',
        u'o' : 'Latin',
        u'O' : 'Latin',
        u'ö' : 'Latin',
        u'Ö' : 'Latin',
        u'Ó' : 'Latin',
        u'ó' : 'Latin',
        u'ő' : 'Latin',
        u'Ô' : 'Latin',
        u'ô' : 'Latin',
        u'p' : 'Latin',
        u'P' : 'Latin',
        u'q' : 'Latin',
        u'Q' : 'Latin',
        u'r' : 'Latin',
        u'R' : 'Latin',
        u'ŕ' : 'Latin',
        u'ř' : 'Latin',
        u'Ř' : 'Latin',
        u's' : 'Latin',
        u'S' : 'Latin',
        u'ß' : 'Latin',
        u'Š' : 'Latin',
        u'š' : 'Latin',
        u't' : 'Latin',
        u'T' : 'Latin',
        u'ť' : 'Latin',
        u'Ť' : 'Latin',
        u'u' : 'Latin',
        u'U' : 'Latin',
        u'ü' : 'Latin',
        u'Ü' : 'Latin',
        u'ú' : 'Latin',
        u'Ú' : 'Latin',
        u'ů' : 'Latin',
        u'Ů' : 'Latin',
        u'v' : 'Latin',
        u'V' : 'Latin',
        u'W' : 'Latin',
        u'w' : 'Latin',
        u'X' : 'Latin',
        u'x' : 'Latin',
        u'y' : 'Latin',
        u'Y' : 'Latin',
        u'ý' : 'Latin',
        u'Ý' : 'Latin',
        u'z' : 'Latin',
        u'Z' : 'Latin',
        u'ż' : 'Latin',
        u'ž' : 'Latin',
        u'Ž' : 'Latin',
        u'Я' : 'Cyrillic',
        u'к' : 'Cyrillic',
        u'у' : 'Cyrillic',
        u'й' : 'Cyrillic',
        u'ж' : 'Cyrillic',
        u'Ш' : 'Cyrillic',
        u'µ' : 'Greek',
        u'אָ' : 'Hebrew'
    }[u_c]

def correct_unicharset(inputfile):
    """ Open unicharset data file and correct script name"""
    filein = codecs.open(inputfile, encoding='utf-8')
    newlines = ""
    for line in filein:
        data = line.strip().split(' ')
        if (len(data) == 4):  # 3.00 version
            if (data[2] == "NULL"):
                try:
                    script_name = find_script_name(data[0])
                    newlines += "%s %s %s %s\n" % (data[0], data[1], \
                                    script_name, data[3])
                except KeyError:
                    # print u"%s is not in the list." % (sys.exc_value)
                    newlines += line 
        elif (len(data) >= 8):   # 3.01 version?
            if (data[3] == "NULL"):
                try:
                    data[3] = find_script_name(data[0])
                except KeyError:
                    pass
            for i in range(len(data)):
                newlines += "%s " % data[i]
            newlines = newlines[:-1] + "\n"
        else:
            newlines += line 
    filein.close()

    file_o = codecs.open(inputfile, encoding='utf-8', mode='w+')
    for line in newlines:
        file_o.write(line)
    file_o.close()
