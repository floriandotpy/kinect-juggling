#!/usr/bin/env python

'''
    Based on demo_freenect.py from the https://github.com/amiller/libfreenect-goodies.git
'''

from freenect import sync_get_depth as get_depth, sync_get_video as get_video
import cv
import numpy as np
from PIL import Image
import random
import time
import imgtools


class Kinector(object):
    """ Does awesome stuff with the Kinect. """
    def __init__(self, buffersize=3, swapbackground=True, disco=False, dummymode=False, showoverlay=False, detectball=False, record=False, canny=False):
        self.running = True
        self.smoothBuffer = imgtools.SmoothBuffer(buffersize)
        self.swapbackground = swapbackground
        self.disco = disco
        self.dummymode = dummymode
        self.showoverlay = showoverlay
        self.threshold = np.empty(shape=(480, 640, 3)).fill(50)
        self.detectball = detectball
        self.balldetector = imgtools.BallDetector([180, 30, 30], threshold=100)
        self.record = record
        if self.dummymode:
            self.depth_0 = np.load("frames/frame-1368712006486-depth.npy")
            self.rgb_0 = np.load("frames/frame-1368712006486-rgb.npy")
        self.canny = canny

    def loop(self):
        """ Start the loop which is terminated by hitting a random key. """
        while self.running:
            if self.record:
                self.snapshot()
            else:
                self._step()
            key = cv.WaitKey(5)
            self.running = key in (-1, 32)
            if key == 32: # space bar
                self.snapshot()

    def snapshot(self):
        (rgb, _) = get_video()
        (depth,_) = get_depth(format=4)
        imgtools.snapshot(rgb, depth)
        # filename = "snapshot-%d.png" % int(time.time()*1000)
        # imgtools.saveImg(rgb, filename)


    def _step(self):
        """ One step of the loop, do not call on its own. Please. """
        # Get a fresh frame
        (depth,_) = get_depth(format=4)
        (rgb,_) = imgtools.getDummyImg("snapshot-1367500340985.png") if self.dummymode else get_video()
        # depth = self.depth_0
        # rgb = self.rgb_0

        # Normalize depth values to be 0..255 instead of 0..2047
        # depth = depth / 8

        # self.smoothBuffer.add(depth)
        # depth = self.smoothBuffer.get()

        if self.swapbackground:
            rgb = imgtools.replaceBackground(rgb, depth, 'bg.jpg')

        if self.disco:
            rgb = imgtools.discoMode(rgb)

        if self.canny:
            depth_opencv = imgtools.canny(depth, as_cv=True)
        else:
            depth_opencv = cv.fromarray(np.array(depth[:,:], dtype=np.uint8))

        # show holes
        depth = imgtools.detectHoles(depth)
        depth = depth / 8
        # depth = self.balldetector.drawRects(rgb, depth)
        depth_opencv = cv.fromarray(np.array(depth[:,:], dtype=np.uint8))


        if self.showoverlay:
            # get center color value
            color = rgb[240, 320]

            # set center marker
            rgb[240, 320] = np.array([255,0,255])

        if self.detectball:
            rgb = self.balldetector.detectDepth(rgb, depth)

        # generate opencv image
        img = cv.fromarray(np.array(rgb[:,:,::-1], dtype=np.uint8))


        if self.showoverlay:
            f = cv.InitFont(cv.CV_FONT_HERSHEY_PLAIN, 1.0, 1.0)
            # PutText(img, text, org, font, color)
            cv.PutText(img, 'Color: %s' % (color), (20,20) , f, (int(color[2]), int(color[1]), int(color[0])))
            cv.PutText(img, 'X', (320, 240) , f, (255, 255 , 255))

        # Display image
        # cv.ShowImage('display', cv.fromarray(np.array(rgb[:,:,::-1])))
        cv.ShowImage('display', depth_opencv)

if __name__ == '__main__':
    Kinector(swapbackground=True, dummymode=False, detectball=False, record=False, canny=False).loop()

