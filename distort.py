#!/usr/local/bin/python
#-*- coding:utf8 -*-
""" This module distorts images
    """

from PIL import Image


def distort(filename2, bbox, akshar):
    """ Distrort image"""
    #temp_image = Image.open(filename2)
    #distort1  =  ImageOps.mirror(temp_image)
    filename = filename2.split('.tif')[0] + "_1" + ".tif"
    #distort1.save(filename, "TIFF")
    #distort2 = Image.open(filename2)

    del_x = bbox[2] - bbox[0]
    strip = [bbox[0] + del_x * .2, bbox[0] + del_x * .4, bbox[0] + del_x * .7]
    for values in range(0, 3):
        distort2 = Image.open(filename2)
        for y_val in range(bbox[1], bbox[3]):
            for x_val in range(strip[values], strip[values] + 4):
                distort2.putpixel((x_val, y_val), 255)
        filename = filename2.split('.tif')[0] + "_" + str(values) + ".tif"
        distort2.save(filename, "TIFF")
        # This is the line to be added to the box file
        line = akshar + " " + str(bbox[0]) + " " + str(bbox[1]) + " " + \
                str(bbox[2]) + " " + str(bbox[3])
        boxfile = filename.split('.tif')[0] + "box"
        f_box = open(boxfile, "w")
        f_box.write(line + '\n')
        f_box.close()
