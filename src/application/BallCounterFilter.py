"""
    A first application example: Determine the actual number
    of balls in the current juggling pattern.
"""

import math

class BallCounterFilter(object):
    def __init__(self):
        self.ballcounter = BallCounter()

    def filter(self, rgb, depth, balls, args={}):
        self.ballcounter.update(balls)

        args['ballcounter'] = self.ballcounter

        return rgb, depth, balls

class BallCounter(object):
    """Determine the actual number of objects in the juggling pattern."""
    def __init__(self):
        self.count = None
        self.last = []
        self.length = 15 # how many frames to analyse

    def update(self, balls):
        self.last.append(len(balls))
        if len(self.last) > self.length:
            self.count = sum(self.last[::-1][:self.length]) / (self.length*1.0)
            self.count = int(math.ceil(self.count)) + 1