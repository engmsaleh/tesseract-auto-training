#!/usr/local/bin/python
#-*- coding:utf8 -*-
""" Test script for creating image with text """

import os
import cairo
import pango
import pangocairo
from PIL import Image, ImageDraw, ImageChops


def main():
    """Main"""
    #The lines below are pango/cairo code
    surface = cairo.ImageSurface(cairo.FORMAT_A8, 400, 100)
    context = cairo.Context(surface)

    pango_cntx = pangocairo.CairoContext(context)

    layout = pango_cntx.create_layout()
    layout.set_font_description(pango.FontDescription('Sans 15'))
    layout.set_text("0 1 2 3 4 5 6 7 8 9 10\na A b B c C d D h H m M")
    
    #layout.set_font_description(pango.FontDescription('Lohit Bengali 10'))
    # layout.set_text("কুকুর হাহা কুকুর" + \
        # " হাহা কুকুর হাহা কুকুর " + \
        # "হাহা কুকুর হাহা কুকুর " + \
        # "হাহা কুকুর হাহা কুকুর " + \
        # "হাহা\n কি হল কি হল" + \
        # " কি হল কি হল কি হল কি" + \
        # " হল কি হল কি হল কি " + \
        # "হল কি হল কি হল কি হল কি হল")

    # Next four lines take care of centering the text. Feel free to ignore ;-)
    #width, height = surface.get_width(), surface.get_height()
    #w, h = layout.get_pixel_size()
    position = (10, 10)  # (width/2.0 - w/2.0, height/2.0 - h/2.0)
    context.move_to(position[0], position[1])
    #context.move_to(*position)
    pango_cntx.show_layout(layout)
    surface.write_to_png("text")

    temp_image = Image.open("text")  # Black background, white text
    #draw = ImageDraw.Draw(temp_image)
    #bbox = temp_image.getbbox()
    #print bbox
    # White background, black text
    inverted_image = ImageChops.invert(temp_image)
    # Lets transfer "draw" to the new image
    #draw = ImageDraw.Draw(inverted_image)
    #draw.rectangle(bbox,None,100) #draw the bounding box

    # Save the symbol to a file
    inverted_image.save("single.tif", "TIFF", dpi=(600, 600))
    os.unlink("text")

if __name__ == '__main__':
    main()
