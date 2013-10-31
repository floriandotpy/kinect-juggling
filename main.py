#!/usr/bin/env python

'''
    Based on demo_freenect.py from the https://github.com/amiller/libfreenect-goodies.git
'''

import cv
import numpy as np
from NoFilter import NoFilter
from BackgroundFilter import BackgroundFilter
from RectsFilter import RectsFilter
from DiscoFilter import DiscoFilter
from OverlayFilter import OverlayFilter
from CannyFilter import CannyFilter
import imgtools


class Kinector(object):
    """ Does awesome stuff with the Kinect. """
    def __init__(self, kinect, filters=[], dummymode=False, buffersize=3, showoverlay=False, record=False, canny=False, hough=False):
        self.running = False
        self.kinect = kinect
        self.smoothBuffer = imgtools.SmoothBuffer(buffersize)
        self.dummymode = dummymode
        self.showoverlay = showoverlay
        self.threshold = np.empty(shape=(480, 640, 3)).fill(50)
        self.balldetector = imgtools.BallDetector([180, 30, 30], threshold=100)
        self.record = record
        self.canny = canny
        self.hough = hough


        self.filters = []

        if 'swapbackground' in filters:
            self.filters.append(BackgroundFilter('bg.jpg'))

        if 'disco' in filters:
            self.filters.append(DiscoFilter())

        if 'canny' in filters:
            self.filters.append(CannyFilter())

        if 'detectball' in filters:
            self.filters.append(RectsFilter())

        self.filters.append(NoFilter())

        if 'overlay' in filters:
            self.filters.append(OverlayFilter())

    def loop(self):
        """ Start the loop which is terminated by hitting a random key. """
        self.running = True
        while self.running:
            if self.record:
                self.kinect.snapshot()
            else:
                self._step()
            key = cv.WaitKey(5)
            self.running = key in (-1, 32)
            if key == 32: # space bar
                self.kinect.snapshot()

    def _step(self):
        """ One step of the loop, do not call on its own. Please. """
        # Get a fresh frame
        (rgb, depth) = self.kinect.get_frame()

        # reduce depth from 2048 to 256 values
        depth = depth / 8

        args = {}
        args['color'] = rgb[240, 320]

        for filter in self.filters:
            rgb, depth = filter.filter(rgb, depth, args)

        # Generate opencv image
        rgb_opencv = cv.fromarray(np.array(rgb[:,:,::-1]))

        # Display image
        cv.ShowImage('display', rgb_opencv)

if __name__ == '__main__':
    import sys

    filters = []
    for argv in sys.argv:
        if argv.startswith('--'):
            filters.append(argv[2:])

    dummymode = "--dummymode" in sys.argv or "-d" in sys.argv
    if dummymode:
        from KinectDummy import KinectDummy
        kinect = KinectDummy()
    else:
        try:
            from Kinect import Kinect
            kinect = Kinect()
        except ImportError:
            from KinectDummy import KinectDummy
            kinect = KinectDummy()
            dummymode = True;

    Kinector(kinect=kinect, filters=filters, dummymode=dummymode, record=False, canny=False, hough=False).loop()

