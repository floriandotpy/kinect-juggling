#!/usr/bin/env python

'''
    Based on demo_freenect.py from the https://github.com/amiller/libfreenect-goodies.git
'''

from freenect import sync_get_depth as get_depth, sync_get_video as get_video
import cv
import numpy as np
from PIL import Image
import random
import imgtools


class Kinector(object):
    """ Does awesome stuff with the Kinect. """
    def __init__(self, buffersize=3, swapbackground=True, disco=False):
        self.running = True
        self.smoothBuffer = imgtools.SmoothBuffer(buffersize)
        self.swapbackground = swapbackground
        self.disco = disco

    def loop(self):
        """ Start the loop which is terminated by hitting a random key. """
        while self.running:
            self._step()
            self.running = cv.WaitKey(5) is -1

    def _step(self):
        """ One step of the loop, do not call on its own. Please. """
        # Get a fresh frame
        (depth,_), (rgb,_) = get_depth(), get_video()

        # Normalize depth values to be 0..255 instead of 0..2047
        depth = depth / 8

        self.smoothBuffer.add(depth)
        depth = self.smoothBuffer.get()

        if self.swapbackground:
            rgb = imgtools.replaceBackground(rgb, depth, 'bg.jpg')

        if self.disco:
            rgb = imgtools.discoMode(rgb)

        # Display image
        cv.ShowImage('display', cv.fromarray(np.array(rgb[:,:,::-1])))
        
if __name__ == '__main__':
    Kinector().loop()

