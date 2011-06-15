#!/usr/local/bin/python
#-*- coding:utf8 -*-
#This code generates the training files for tesseract-ocr for bootstrapping a new character set
import file
import distort
import train

import os
import sys

#from Sayamindu's code
import cairo
import pango
import pangocairo

import ImageFont, ImageDraw, ImageChops
from PIL import Image


bigbox=()


def expand(temp_bbox):
    """expand a bounding box a little bit"""
    tol=2
    bbox=(temp_bbox[0]-tol,temp_bbox[1]-tol,temp_bbox[2]+tol,temp_bbox[3]+tol)
    return bbox


def draw(font_string,font_size,lang,alphabets): # language, font file name, font full path, font size, characters
    """ Generates tif images and box files"""
    
    
    image_dir=lang+"."+"images"
    if(os.path.exists(image_dir)):
        pass
    else:
        os.mkdir(image_dir)
       
    #Using a font
    #font= ImageFont.truetype(font,fsz)
    boxfile=image_dir+"/"+"bigimage.box"
    f=open(boxfile,"w")
     
    bigimage=Image.new("L",(2000,2000),255)
    bigdraw=ImageDraw.Draw(bigimage)
    x=y=10
    count=0
    for akshar in alphabets:
        akshar.strip() #remove nasty characters
       
        #I shall now create an image with black bgc and white font color. One
        #getbbox() determines the bounding box values I shall invert the image.
        #This has to be done since getbbox() only finds bounding box values for
        #non-zero pixels (read as white), but tesseract-ocr runs on the exact
        #opposite bgc fgc combination. Contact debayanin@gmail.com.
      
       
        #The lines below are pango/cairo code
        surface = cairo.ImageSurface(cairo.FORMAT_A8, font_size*4, font_size*3)
        context = cairo.Context(surface)

        pc = pangocairo.CairoContext(context)

        layout = pc.create_layout()
        layout.set_font_description(pango.FontDescription(font_string))
        layout.set_text(akshar)
        print akshar

        #  lines take care of centering the text.
        width, height = surface.get_width(), surface.get_height()
        w, h = layout.get_pixel_size()
        position = (10,10)#(width/2.0 - w/2.0, height/2.0 - h/2.0)
        context.move_to(*position)
        pc.show_layout(layout)
        surface.write_to_png("pango.png")
	#iter=layout.get_iter()
	#print iter.get_char_extents()

        #Here we open the generated image using PIL functions
        temp_image=Image.open("pango.png") #black background, white text
        draw = ImageDraw.Draw(temp_image)
        bbox = temp_image.getbbox()
        deltax=bbox[2]-bbox[0]
        deltay=bbox[3]-bbox[1]

       
        print bbox
        new_image=temp_image.crop(bbox)
        temp_image=temp_image.load()
        inverted_image = ImageChops.invert(new_image) #White background, black text
	
	inverted_image.save(image_dir+"/"+str(count)+".png")
	count=count+1
	

        bigimage.paste(inverted_image,(x,y))
	#bigimage.load()
        bigbox=(x,y,x+deltax,y+deltay)
        print bigbox
        draw=ImageDraw.Draw(bigimage)
	#draw.rectangle(bigbox,None,100)
        x=bigbox[2]+5
        if x>1950:
            x=10; y=y+40

        os.unlink("pango.png") #delete the pango generated png

        line=akshar+" "+str(bigbox[0]-1)+" "+str(2000-(bigbox[1]+deltay)-1)+" "+str(bigbox[2]+1)+" "+str(2000-(bigbox[3]-deltay)+1) # this is the line to be added to the box file
	f.write(line+'\n')

	#degrade code starts
	strip=[deltax*.2,deltax*.4,deltax*.7]
	for values in range(0,3):
		distort2=inverted_image
		for wai in range(0,deltay):
			for ex in range(strip[values],strip[values]+1):
				distort2.putpixel((ex,wai),255)
		bigbox=(x,y,x+deltax,y+deltay)
		#draw.rectangle(bigbox,None,10)
		line=akshar+" "+str(bigbox[0]-1)+" "+str(2000-(bigbox[1]+deltay)-1)+" "+str(bigbox[2]+1)+" "+str(2000-(bigbox[3]-deltay)+1) # this is the line to be added to the box file
        	f.write(line+'\n')
		bigimage.paste(distort2,(x,y))
		x=bigbox[2]+5
        	if x>1950:
            		x=10; y=y+40
		
			
	#degrade code ends
     
        #distort.distort(filename2,bbox,fsz,akshar)
     
       
       
    bigimage.save(image_dir+"/"+"bigimage.tif","TIFF")
    f.close()
       
           
if(len(sys.argv)!=9):
    print "Usage: python generate.py -font <font name> -l <language> -s <size> -a <input alphabet directory>"
    exit()

if(sys.argv[1]=="-font"):
    font_name=sys.argv[2]
else:
    print "Usage: python generate.py -font <font name> -l <language> -s <size> -a <input alphabet directory>"
    exit()
       
if(sys.argv[3]=="-l"):
    lang=sys.argv[4]
else:
    print "Usage: python generate.py -font <font name> -l <language> -s <size> -a <input alphabet directory>"
    exit()
   
if(sys.argv[5]=="-s"):
    font_size=sys.argv[6]
else:
    print "Usage: python generate.py -font <font name> -l <language> -s <size> -a <input alphabet directory>"
    exit()

if(sys.argv[7]=="-a"):
    alphabet_dir=sys.argv[8]
else:
    print "Usage: python generate.py -font <font name> -l <language> -s <size> -a <input alphabet directory>"
    exit()

font_string=font_name+" "+lang+" "+font_size


#begin training    
draw(font_string,int(font_size),lang,file.read_file(alphabet_dir))#reads all fonts in the directory font_dir and trains

train.train(lang)
#training ends


