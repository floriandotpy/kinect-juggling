#!/usr/bin/env python

import numpy as np
import time
import cv
import cv2
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

# ball detection, hand tracking
from src.balldetection.SimpleBall import SimpleBallFilter
from src.balldetection.SimpleHandBall import SimpleHandBallFilter
from src.balldetection.TrajectoryBall import TrajectoryBallCollection
from src.balldetection.PreciseTrajectoryBall import PreciseTrajectoryBallCollection
from src.balldetection.MinimalBall import MinimalBallFilter
from src.balldetection.HandTracking import HandTrackingFilter

# visualization
from src.visual.DrawBallsFilter import DrawBallsFilter
from src.visual.SlowmotionFilter import SlowmotionFilter
from src.visual.RgbDepthFilter import RgbDepthFilter

# application
from src.application.KalmanFilter import KalmanFilter
from src.application.BallCounterFilter import BallCounterFilter


class Kinector(object):
    """ Does awesome stuff with the Kinect. """
    def __init__(self, kinect, args=[]):
        self.running = False
        self.record = 'record' in args
        self.show = 'depth' if 'depth' in args else 'rgb'
        self.paused = False
        self.kinect = kinect

        # track hands

        # init filters
        self.filters = []

        # preprocessing
        if 'withholes' not in args:
            self.filters.append(DepthHolesFilter())
        if 'swapbackground' in args:
            self.filters.append(BackgroundFilter('bg.jpg'))
        if 'canny' in args:
            self.filters.append(CannyFilter())
        if 'cutoff' in args:
            self.filters.append(CutOffFilter())
        if 'detectball' in args:
            self.filters.append(RectsFilter())

        # ball detection
        if 'handtracking' in args:
            self.filters.append(HandTrackingFilter())
        if 'minimal' in args:
            self.filters.append(MinimalBallFilter())
        elif 'simplehand' in args:
            self.filters.append(SimpleHandBallFilter())
        else:
            self.filters.append(SimpleBallFilter())


        # application
        if 'countballs' in args:
            self.filters.append(BallCounterFilter())

        # visualization
        if 'detectball' in args:
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

            self.running = key in (-1, 32, 112)

            # "p" pressed: pause/unpause
            self.paused = not self.paused if (key == 112) else self.paused

            # space bar: take snapshot
            snapshot = (key == 32)

            if not self.paused:
                self._step(snapshot)

    def snapshot(self, rgb):
        filename = "snapshots/frame-%d.png" % int(time.time()*1000)

        im = Image.fromarray(rgb)
        im.save(filename)

    def _step(self, snapshot=False):
        """ One step of the loop, do not call on its own. Please. """
        # Get a fresh frame
        (rgb, depth) = self.kinect.get_frame(record=self.record)
        balls = []

        args = {}

        # where we will collect our balls
        # FIXME: needed in each step?
        # args['balls'] = self.ballcollection
        # args['hands'] = self.hands

        for filter in self.filters:
            rgb, depth, balls = filter.filter(rgb, depth, balls, args)


        if self.show == 'rgb':
            # Generate opencv image
            img = cv.fromarray(np.array(rgb[:,:,::-1]))
        else:
            # reduce depth from 2048 to 256 values
            depth = depth / 8

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
            from src.kinect.KinectDummy import KinectDummy
            kinect = KinectDummy()

    Kinector(kinect=kinect, args=args).loop()

