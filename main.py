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
from CutOffFilter import CutOffFilter
import imgtools


class Kinector(object):
    """ Does awesome stuff with the Kinect. """
    def __init__(self, kinect, args=[], buffersize=3):
        self.running = False
        self.record = 'record' in args
        self.show = 'depth' if 'depth' in args else 'rgb'

        self.kinect = kinect

        # TODO: implement useful buffer
        # self.smoothBuffer = imgtools.SmoothBuffer(buffersize)


        # init filters
        self.filters = []
        if 'swapbackground' in args:
            self.filters.append(BackgroundFilter('bg.jpg'))
        if 'disco' in args:
            self.filters.append(DiscoFilter())
        if 'canny' in args:
            self.filters.append(CannyFilter())
        if 'detectball' in args:
            self.filters.append(CutOffFilter())
            self.filters.append(RectsFilter())
        if 'overlay' in args:
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

        for filter in self.filters:
            rgb, depth = filter.filter(rgb, depth, args)


        if self.show == 'rgb':
            # Generate opencv image
            img = cv.fromarray(np.array(rgb[:,:,::-1]))
        else:
            # reduce depth from 4096 to 256 values
            depth = depth / 16

            a = np.ndarray(shape=(480,640,3), dtype=np.uint8)
            a[:,:,0] = depth
            a[:,:,1] = depth
            a[:,:,2] = depth
            img = cv.fromarray(a)
            # print a[200:205,200:205]
            # image(img,0,0)


        # Display image
        cv.ShowImage('display', img)

if __name__ == '__main__':
    import sys

    args = []
    for argv in sys.argv:
        if argv.startswith('--'):
            args.append(argv[2:])

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

    Kinector(kinect=kinect, args=args).loop()

