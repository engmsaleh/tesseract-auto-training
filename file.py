#This code reads alphabet characters from certain files and fills up an array so
#it can be used for generating test images

import os

def combine(frest,fc,fpresv,fpostsv):
    """ Creates all possible combinations of consonant+vowel"""
    all_comb=[]
    
    for rest in frest:
        rest=rest.strip()
        all_comb.append(rest)
    
    for c in fc:
        c=c.strip() #remove special characters
        c1=c+" "
        all_comb.append(c1)
        for prev in fpresv:  # combine consonant+vowel sign
            txt=prev.rstrip()+c
            all_comb.append(txt)
        for postv in fpostsv: # combine vowel sign+consonant
            txt=c+postv.strip()
            txt=txt+" "
            all_comb.append(txt)
    count=0
    for a in all_comb:
        #print count,
        count+=1
        print a
    return all_comb



def read_file(alphabet_dir):
    """Reads input alphabet files from alphabet_dir"""
    print "in file.py"
    #file containing vowels
    if(os.path.exists(alphabet_dir+"consonants_conjuncts")):
        f=open(alphabet_dir+"consonants_conjuncts",'r')
        fc=f.readlines()
        f.close()
    else:
        fc=[]
        
    
    #file containing semivowels of the form consonant_conjunct+semivowel	
    if(os.path.exists(alphabet_dir+"pre_semivowels")):
        f=open(alphabet_dir+"pre_semivowels",'r')
        fpresv=f.readlines()
        f.close()
    else:
        fpresv=[]
        

    #file containing semivowels of the form semivowel+consonant_conjunct
    if(os.path.exists(alphabet_dir+"post_semivowels")):
        f=open(alphabet_dir+"post_semivowels",'r')
        fpostsv=f.readlines()
        f.close()
    else:
        fpostsv=[]
    
    #file containing everything else
    if(os.path.exists(alphabet_dir+"rest")):
        f=open(alphabet_dir+"rest",'r')
        frest=f.readlines()
        f.close()
    else:
        frest=[]
    return combine(frest,fc,fpresv,fpostsv)
