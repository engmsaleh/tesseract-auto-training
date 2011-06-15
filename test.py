#!/usr/local/bin/python
#-*- coding:utf8 -*-

import os
import sys

#from Sayamindu's code
import cairo
import pango
import pangocairo
import ImageFont, ImageDraw, ImageChops
from PIL import Image




#The lines below are pango/cairo code
surface = cairo.ImageSurface(cairo.FORMAT_A8, 400, 100)
context = cairo.Context(surface)

pc = pangocairo.CairoContext(context)

layout = pc.create_layout()
layout.set_font_description(pango.FontDescription('Lohit Bengali 15'))
layout.set_text("কুকুর হাহা কুকুর হাহা কুকুর হাহা কুকুর হাহা কুকুর হাহা কুকুর হাহা কুকুর হাহা কুকুর হাহা\n কি হল কি হল কি হল কি হল কি হল কি হল কি হল কি হল কি হল কি হল কি হল কি হল কি হল")


# Next four lines take care of centering the text. Feel free to ignore ;-)
width, height = surface.get_width(), surface.get_height()
w, h = layout.get_pixel_size()
position = (10,10)#(width/2.0 - w/2.0, height/2.0 - h/2.0)
context.move_to(*position)
pc.show_layout(layout)
surface.write_to_png("text")

temp_image=Image.open("text") #black background, white text
draw = ImageDraw.Draw(temp_image)
bbox = temp_image.getbbox()
#print bbox
inverted_image = ImageChops.invert(temp_image) #White background, black text
draw= ImageDraw.Draw(inverted_image)      #Lets transfer "draw" to the new image
#draw.rectangle(bbox,None,100) #draw the bounding box
inverted_image.save("single.tif","TIFF")#save the symbol to a file
os.unlink("text")
