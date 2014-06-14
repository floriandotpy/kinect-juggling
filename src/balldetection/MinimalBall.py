"""
MinimalBall.py
---
A minimal ball detection. This is very plain and just there to
show an example of how the interface of the Ball Detection
should look like.
"""

# tmp
import cv
import numpy as np
import random
from src.Util import getcolour
from src.balldetection.Ball import Ball

class MinimalBallFilter(object):

    def __init__(self):
        self.balls = []

    def filter(self, rgb, depth, ball_list, args = {}):

        # first call?
        if len(self.balls) == 0:
            # only instantiate balls if we have 3 positions right now
            if len(ball_list) == 3:
                for ball in ball_list:
                    self.balls.append(Ball(ball['position'], radius=ball['radius']))
        else: # find the correct ball to update
            # minmal (bad) solution: just pick any position
            for i in xrange(len(self.balls)):
                if i < len(ball_list):
                    self.balls[i].updatePosition(ball_list[i]['position'])

        return rgb, depth, self.balls





