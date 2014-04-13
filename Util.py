'''
Util.py
---
utility functions
'''

import cv

colours = [cv.RGB(0, 0, 255), cv.RGB(0, 255, 0), cv.RGB(255, 0, 0), cv.RGB(0, 255, 255), cv.RGB(255, 0, 255)]
util_color_index = 0

def getcolour():
    global util_color_index
    colour = colours[util_color_index]
    util_color_index = (util_color_index + 1) % len(colours)
    return colour
