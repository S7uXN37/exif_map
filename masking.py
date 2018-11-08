'''
Given an image in RGB or RGBA, functions in masking will return a masked RGBA image.
'''

import numpy
from PIL import Image

__author__ = "S7uXN37"
__license__ = "MIT"
__copyright__ = "Copyright 2018, Marc Himmelberger"

def circle(img):
    w,h = img.size
    r = min(w,h)/2.0
    pix = numpy.array(img)
    img_new = numpy.array((h,w,4))
    for y, row in enumerate(pix):
        for x, pixel in enumerate(row):
            for i, val in enumerate(pixel):
                img_new[y,x,i] = val
            img_new[y,x,3] = 255 if pow(r,2) > pow(x-w/2,2) + pow(y-h/2, 2) else 0
    return Image.fromarray(img_new)
            
