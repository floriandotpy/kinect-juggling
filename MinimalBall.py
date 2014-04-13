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
from Util import getcolour


class MinimalBall(object):
    """docstring for Ball"""
    def __init__(self, position, radius=10, meta=None):
        self.colour = getcolour()
        self.position = position
        self.radius = radius
        self.meta = meta
        self.positions = [] # collect older positions

    def updatePosition(self, ball, radius=10):
        self.positions = self.positions[:2] # keep positions list short
        self.positions.append(self.position)
        self.position = ball['position']
        self.radius = radius

    def futurePosition(self, trajectory=False):
        # this one doesnt to future predction, return current position instead
        return self.position

    def __str__(self):
        return "Ball at %d/%d" % self.position


class MinimalBallCollection(object):
    def __init__(self):
        self.balls = []

    def addPositions(self, ball_list):

        # first call?
        if not len(self.balls):
            # only instantiate balls if we have 3 positions right now
            if len(ball_list) != 3:
                return
            for ball in ball_list:
                self.balls.append(MinimalBall(ball['position'], radius=ball['radius']))
        else: # find the correct ball to update
            # minmal (bad) solution: just pick any position
            for i in xrange(len(self.balls)):
                if i < len(ball_list):
                    self.balls[i].updatePosition(ball_list[i])



