#!/usr/bin/env python

'''
    Based on demo_freenect.py from the https://github.com/amiller/libfreenect-goodies.git
'''

from freenect import sync_get_depth as get_depth, sync_get_video as get_video
import cv
import numpy as np
from PIL import Image
import random

def doloop():
    # load background image
    img = np.asarray(Image.open('bg.jpg'))

    global depth, rgb
    running = True

    # parallax offset, can be removed as soon as we switch to unstable
    x, y = 54, 50

    while running:
        # Get a fresh frame
        (depth,_), (rgb,_) = get_depth(), get_video()

        # Normalize depth values to be 0..255 instead of 0..2047
        depth = depth / 8
        
        # Build a two panel color image
        d3 = np.dstack((depth,depth,depth)).astype(np.uint8)

        # Remove the background based on the depth field
        subset = depth > 100
        subset[y:,:-x] = subset[:-y,x:]
        subset[:,-x:] = True
        subset[:y,:] = True
        rgb[subset] = img[subset]

        # Shuffle RGB channels for every pixel
        l = [0,1,2]
        random.shuffle(l)
        mapping = ([0, 1, 2], l)
        rgb[:,:,mapping[0][0]], rgb[:,:,mapping[0][1]], rgb[:,:,mapping[0][1]] = rgb[:,:,mapping[1][0]], rgb[:,:,mapping[1][1]], rgb[:,:,mapping[1][2]]

        # Simple Downsample and show both
        # da = np.hstack((d3,rgb))
        # cv.ShowImage('both', cv.fromarray(np.array(da[::2,::2,::-1])))

        # Show modified rgb image in full resolution
        cv.ShowImage('display', cv.fromarray(np.array(rgb[:,:,::-1])))
        running = cv.WaitKey(5) is -1
        
doloop()

