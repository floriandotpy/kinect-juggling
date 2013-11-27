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
from DepthHolesFilter import DepthHolesFilter
from MaximaFilter import MaximaFilter
from HoughFilter import HoughFilter
from TemporalFilter import TemporalFilter
from DrawBallsFilter import DrawBallsFilter
from Ball import BallCollection
import imgtools


class Kinector(object):
    """ Does awesome stuff with the Kinect. """
    def __init__(self, kinect, args=[], buffersize=3):
        self.running = False
        self.record = 'record' in args
        self.show = 'depth' if 'depth' in args else 'rgb'

        self.kinect = kinect

        # TODO: implement useful buffer
        if 'buffer' in args:
            self.buffer = imgtools.SmoothBuffer(buffersize=2)
        else:
            self.buffer = None


        self.ballcollection = BallCollection()

        # init filters
        self.filters = []

        if 'withholes' not in args:
            self.filters.append(DepthHolesFilter())
        if 'swapbackground' in args:
            self.filters.append(BackgroundFilter('bg.jpg'))
        if 'disco' in args:
            self.filters.append(DiscoFilter())
        if 'canny' in args:
            self.filters.append(CannyFilter())
        if 'detectball' in args:
            self.filters.append(CutOffFilter())
            self.filters.append(RectsFilter())
            self.filters.append(DrawBallsFilter())
        if 'overlay' in args:
            self.filters.append(OverlayFilter())
        if 'maxima' in args:
            self.filters.append(MaximaFilter())
        if 'hough' in args:
            self.filters.append(HoughFilter())
        if 'temporal' in args:
            self.filters.append(TemporalFilter())

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

        args = {}

        # where we will collect our balls
        args['balls'] = self.ballcollection

        if self.buffer:
            self.buffer.add(depth)
            args['buffer'] = self.buffer

        for filter in self.filters:
            rgb, depth = filter.filter(rgb, depth, args)


        if self.show == 'rgb':
            # Generate opencv image
            img = cv.fromarray(np.array(rgb[:,:,::-1]))
        else:
            # reduce depth from 2048 to 256 values
            depth = depth /16
            # print depth[220:225, 280:285]

            a = np.ndarray(shape=(480,640,3), dtype=np.uint8)
            a[:,:,0] = depth
            a[:,:,1] = depth
            a[:,:,2] = depth
            img = cv.fromarray(a)


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

