import os
import string
import shutil

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
    
    

def train(lang):
    """Generates normproto, inttemp, Microfeat, unicharset and pffmtable"""
    output_dir=lang+"."+"training_data"
    dir=lang+"."+"images"+"/"
    
    if(os.path.exists(output_dir)):
        pass
    else:
        os.mkdir(output_dir)
   # os.chdir(output_dir)
    print "in train"
    image='bigimage.tif'
    box='bigimage.box'
    exec_string1='tesseract '+dir+image+' junk nobatch box.train'
    print exec_string1
    qpipe = os.popen4(exec_string1) #This returns a list.  The second list element is a file object from which you can read the command output.
    o=qpipe[1].readlines() 
    pos=str(o).find('FAILURE') #Look for the word "FAILURE" in tesseract-ocr trainer output.
    print str(o)
    print " ok ",
            
                       
    #now begins clustering
    
    exec_string2="mftraining"
    exec_string3="cntraining"
    
    #os.chdir(lang+".training_data")
    
    for t in os.walk(dir):
        for f in t[2]:
            if(f.split('.')[1]=="tr"):
                exec_string2+=" "+dir+f+" "
                exec_string3+=" "+dir+f+" "
    qpipe2=os.popen4(exec_string2)
    qpipe3=os.popen4(exec_string3)
    #clustering ends
    
    #unicharset_extractor begins
    exec_string4="unicharset_extractor"
    for t in os.walk(dir):
        for f in t[2]:
            if(f.split('.')[1]=="box"):
                exec_string4+=" "+dir+f
                print exec_string4
    qpipe4=os.popen4(exec_string4)
    #unicharset_extractor ends
    
    #Now rename the 5 training files so it can be readily used with tesseract
    if(os.path.exists("Microfeat") is True):
        os.rename("Microfeat",lang+".Microfeat")
        shutil.move(lang+".Microfeat",lang+".training_data/")
        print "Microfeat renamed and moved"
        
    if(os.path.exists("inttemp") is True):
        os.rename("inttemp",lang+".inttemp")
        shutil.move(lang+".inttemp",lang+".training_data/")
        print "inttemp renamed and moved"
        
    if(os.path.exists("normproto") is True):
        os.rename("normproto",lang+".normproto")
        shutil.move(lang+".normproto",lang+".training_data/")
        print "normproto renamed and moved"
        
    if(os.path.exists("pffmtable") is True):
        os.rename("pffmtable",lang+".pffmtable")
        shutil.move(lang+".pffmtable",lang+".training_data/")
        print "pffmtable renamed and moved"
        
    if(os.path.exists("unicharset") is True):
        os.rename("unicharset",lang+".unicharset")
        shutil.move(lang+".unicharset",lang+".training_data/")
        print "unicharset renamed and moved"
