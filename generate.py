#!/usr/bin/env python
#-*- coding:utf8 -*-
""" This code generates the training files for tesseract-ocr for bootstrapping
    a new character set
    """

import tatfile
import os
import sys
import pango
import cairo
import pangocairo

from PIL import Image, ImageDraw, ImageChops

import train


def expand(temp_bbox):
    """expand a bounding box a little bit"""
    tol = 2
    bbox = (temp_bbox[0] - tol, temp_bbox[1] - tol, temp_bbox[2] + tol, \
          temp_bbox[3] + tol)
    return bbox


def draw(font_name, font_size, lang, alphabets):
    """ Generates tif images and box files"""
    font_string = font_name + ' ' + str(font_size)
    image_dir = lang + "." + "images"

    if(os.path.exists(image_dir)):
        pass
    else:
        os.mkdir(image_dir)

    boxfile = image_dir + "/" + lang + "." + font_name + \
                ".exp%2d.box" % (font_size)
    file_box = open(boxfile, "w")

    # TODO: A4 = 2480x3508 with 300x300 DPI
    # TODO: A5 format 1754x2480 with 300x300 DPI
    bigimage = Image.new("L", (2000, 2000), 255)
    x_val = y_val = 10
    count = 0

    for akshar in alphabets:
        akshar.strip()  # remove nasty characters

        # I shall now create an image with black bgc and white font color. One
        # getbbox() determines the bounding box values I shall invert the
        # image. This has to be done since getbbox() only finds bounding box
        # values for non-zero pixels (read as white), but tesseract-ocr runs on
        # the exact opposite bgc fgc combination. Contact debayanin@gmail.com.

        # The lines below are pango/cairo code
        surface = cairo.ImageSurface(cairo.FORMAT_A8, font_size * 4, \
                                     font_size * 3)
        context = cairo.Context(surface)
        p_context = pangocairo.CairoContext(context)
        layout = p_context.create_layout()
        layout.set_font_description(pango.FontDescription(font_string))
        layout.set_text(akshar)
        #print akshar

        # Lines take care of centering the text.
        position = (10, 10)  # (width/2.0 - w/2.0, height/2.0 - h/2.0)
        context.move_to(position[0], position[1])
        p_context.show_layout(layout)
        surface.write_to_png("pango.png")

        # Here we open the generated image using PIL functions
        # Black background, white text
        temp_image = Image.open("pango.png")
        bbox = temp_image.getbbox()
        deltax = bbox[2] - bbox[0]
        deltay = bbox[3] - bbox[1]
        #print bbox

        new_image = temp_image.crop(bbox)
        temp_image = temp_image.load()
        # White background, black text
        inverted_image = ImageChops.invert(new_image)

        inverted_image.save(image_dir + "/" + str(count) + ".png")
        count = count + 1

        bigimage.paste(inverted_image, (x_val, y_val))
        bigbox = (x_val, y_val, x_val + deltax, y_val + deltay)
        x_val = bigbox[2] + 5
        if x_val > 1950:
            x_val = 10
            y_val = y_val + 40

        # Delete the pango generated png
        os.unlink("pango.png")

        # This is the line to be added to the box file
        line = akshar + " " + str(bigbox[0] - 1) + " " + \
                str(2000 - (bigbox[1] + deltay) - 1) + " " + \
                str(bigbox[2] + 1) + " " + str(2000 - (bigbox[3] - deltay) + 1)
        #print "line:", line
        file_box.write(line + '\n')

        # Degrade code starts
        strip = [deltax * .2, deltax * .4, deltax * .7]
        for values in range(0, 3):
            distort2 = inverted_image
            for wai in range(0, deltay):
                for ex in range(int(strip[values]), int(strip[values]) + 1):
                    distort2.putpixel((ex, wai), 255)
            bigbox = (x_val, y_val, x_val + deltax, y_val + deltay)

            # This is the line to be added to the box file
            line = akshar + " " + str(bigbox[0] - 1) + " " + \
                    str(2000 - (bigbox[1] + deltay) - 1) + " " + \
                    str(bigbox[2] + 1) + " " + \
                    str(2000 - (bigbox[3] - deltay) + 1)
            file_box.write(line + '\n')
            bigimage.paste(distort2, (x_val, y_val))
            x_val = bigbox[2] + 5
            if x_val > 1950:
                x_val = 10
                y_val = y_val + 40
        # Degrade code ends

    # TODO: multipage tiff maybe with:
    #  - http://code.google.com/p/pylibtiff/
    #  - http://freeimagepy.sourceforge.net/
    #  - http://code.google.com/p/pylepthonica/
    bigimage.save(image_dir + "/" + lang + "." + font_name + \
                    ".exp%2d.tif" % font_size, "TIFF", dpi=(600, 600))
    file_box.close()


def main():
    """Main"""
    if(len(sys.argv) != 9):
        print "Usage: python generate.py -font <font name> -l <language> " + \
                "-s <size> -a <input alphabet directory>"
        exit()

    if(sys.argv[1] == "-font"):
        font_name = sys.argv[2]
    else:
        print "Usage: python generate.py -font <font name> -l <language> " + \
                "-s <size> -a <input alphabet directory>"
        exit()

    if(sys.argv[3] == "-l"):
        lang = sys.argv[4]
    else:
        print "Usage: python generate.py -font <font name> -l <language> " + \
                "-s <size> -a <input alphabet directory>"
        exit()

    if(sys.argv[5] == "-s"):
        font_size = sys.argv[6]
    else:
        print "Usage: python generate.py -font <font name> -l <language> " + \
                "-s <size> -a <input alphabet directory>"
        exit()

    if(sys.argv[7] == "-a"):
        alphabet_dir = sys.argv[8]
    else:
        print "Usage: python generate.py -font <font name> -l <language> " + \
                "-s <size> -a <input alphabet directory>"
        exit()

    draw(font_name, int(font_size), lang, tatfile.read_file(alphabet_dir))

    # Begin training
    # Reads all fonts in the directory font_dir and trains
    train.train(lang, lang + "." + font_name + ".exp%2d" % (int(font_size)))
    #training ends

if __name__ == '__main__':
    main()
