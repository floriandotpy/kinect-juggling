#!/usr/bin/env python

'''
    Based on demo_freenect.py from the https://github.com/amiller/libfreenect-goodies.git
'''

import numpy as np
import time
import cv
from PIL import Image

from src.NoFilter import NoFilter

# preprocessing
from src.preprocessing.BackgroundFilter import BackgroundFilter
from src.preprocessing.RectsFilter import RectsFilter
from src.preprocessing.OverlayFilter import OverlayFilter
from src.preprocessing.CannyFilter import CannyFilter
from src.preprocessing.CutOffFilter import CutOffFilter
from src.preprocessing.DepthHolesFilter import DepthHolesFilter
from src.preprocessing.MaximaFilter import MaximaFilter
from src.preprocessing.HoughFilter import HoughFilter
from src.preprocessing.TemporalFilter import TemporalFilter

# ball detection
from src.balldetection.SimpleBall import SimpleBallCollection
from src.balldetection.SimpleHandBall import SimpleHandBallCollection
from src.balldetection.TrajectoryBall import TrajectoryBallCollection
from src.balldetection.PreciseTrajectoryBall import PreciseTrajectoryBallCollection
from src.balldetection.MinimalBall import MinimalBallCollection
from src.balldetection.HandTracking import HandCollection

# visualization
from src.visual.DrawBallsFilter import DrawBallsFilter
from src.visual.SlowmotionFilter import SlowmotionFilter
from src.visual.RgbDepthFilter import RgbDepthFilter

# application
from src.application.KalmanFilter import KalmanFilter


class Kinector(object):
    """ Does awesome stuff with the Kinect. """
    def __init__(self, kinect, args=[]):
        self.running = False
        self.record = 'record' in args
        self.show = 'depth' if 'depth' in args else 'rgb'

        self.kinect = kinect

        # track hands
        self.hands = HandCollection()

        # detected balls are collected
        if 'trajectory' in args:
            self.ballcollection = TrajectoryBallCollection()
        elif 'precise' in args:
            self.ballcollection = PreciseTrajectoryBallCollection()
        elif 'minimal' in args:
            self.ballcollection = MinimalBallCollection()
        elif 'simplehand' in args:
            self.ballcollection = SimpleHandBallCollection()
        else:
            self.ballcollection = SimpleBallCollection()

        # init filters
        self.filters = []

        if 'withholes' not in args:
            self.filters.append(DepthHolesFilter())
        if 'swapbackground' in args:
            self.filters.append(BackgroundFilter('bg.jpg'))
        if 'canny' in args:
            self.filters.append(CannyFilter())
        if 'cutoff' in args:
            self.filters.append(CutOffFilter())
        if 'drawrects' in args:
            self.filters.append(RectsFilter())
        if 'detectball' in args:
            self.filters.append(RectsFilter())
            self.filters.append(DrawBallsFilter())
        if 'overlay' in args:
            self.filters.append(OverlayFilter())
        if 'maxima' in args:
            self.filters.append(MaximaFilter())
        if 'hough' in args:
            self.filters.append(HoughFilter())
        if 'temporal' in args:
            erosion = False if 'noerosion' in args else True
            self.filters.append(TemporalFilter(erosion = erosion))
        if 'slowmotion' in args:
            self.filters.append(SlowmotionFilter(0.4))
        if 'kalman' in args:
            self.filters.append(KalmanFilter())
        if 'showdepth' in args:
            self.filters.append(RgbDepthFilter())

    def loop(self):
        """ Start the loop which is terminated by hitting a random key. """
        self.running = True
        while self.running:
            key = cv.WaitKey(5)
            self.running = key in (-1, 32)

            snapshot = (key == 32) # space bar

            self._step(snapshot)

    def snapshot(self, rgb):
        filename = "snapshots/frame-%d.png" % int(time.time()*1000)

        im = Image.fromarray(rgb)
        im.save(filename)

    def _step(self, snapshot=False):
        """ One step of the loop, do not call on its own. Please. """
        # Get a fresh frame
        (rgb, depth) = self.kinect.get_frame(record=self.record)

        args = {}

        # where we will collect our balls
        # FIXME: needed in each step?
        args['balls'] = self.ballcollection
        args['hands'] = self.hands

        for filter in self.filters:
            rgb, depth = filter.filter(rgb, depth, args)


        if self.show == 'rgb':
            # Generate opencv image
            img = cv.fromarray(np.array(rgb[:,:,::-1]))
        else:
            # reduce depth from 2048 to 256 values
            depth = depth / 16

            a = np.ndarray(shape=(480,640,3), dtype=np.uint8)
            a[:,:,0] = depth
            a[:,:,1] = depth
            a[:,:,2] = depth
            img = cv.fromarray(a)


        if (snapshot):
            self.snapshot(rgb)

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
        from src.kinect.KinectDummy import KinectDummy
        kinect = KinectDummy()
    else:
        try:
            from src.kinect.Kinect import Kinect
            kinect = Kinect()
        except ImportError:
            from kinect.KinectDummy import KinectDummy
            kinect = KinectDummy()
            dummymode = True;

    Kinector(kinect=kinect, args=args).loop()

