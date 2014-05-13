# tmp
import cv
import math
import numpy as np
from Util import getcolour


class SimpleHandBall(object):
    """docstring for Ball"""
    def __init__(self, position, radius=10, meta=None):
        self.colour = getcolour()
        self.position = position
        self.positions = []
        self.radius = radius
        self.meta = meta
        self.updatedAlready = False
        self.closeThreshold = 40 # pixel distance for 2 balls to be considered "close"

    def updatePosition(self, position, radius=10):
        self.positions.append( self.position )
        self.position = position
        self.radius = 10
        self.updatedAlready = True

    def directionVector(self):
        n = 2
        if len(self.positions) < n:
            return (0, 0)
        else:
            # positions = self.positions[:-n]
            # x = sum([p[0] for p in positions])/n
            # y = sum([p[1] for p in positions])/n
            last_pos = self.positions[-1]
            x = self.position[0] - last_pos[0]
            y = self.position[1] - last_pos[1]
            return (x, y)

    def trajectory(self, (x1, y1), (x2, y2), t=1):
        """Calculate the throw trajectory based of 2 points return any future
        or past point on that trajectory"""

        # gravity, positive because y is upside-down
        g   = 9.81 * 0.4

        # speed in x and y direction
        v_x = x2 - x1
        v_y = y2 - y1

        # distance in x and y direction
        x   = v_x * t + x2
        y   = v_y * t + g/2 * t**2 + y2

        return int(x), int(y)

    def lastPosition(self, n=1):
        if len(self.positions > (n-1)):
            return self.positions[-n]
        else:
            return self.position

    def isClose(self, otherBall):
        otherPosition = otherBall['position']
        return self.distance(otherPosition, self.position) < self.closeThreshold
        return (self.distance(otherPosition, self.futurePosition(True)) < self.closeThreshold)

    def futurePosition(self, trajectory=False):
        if trajectory:
            if len(self.positions) < 2:
                return (0, 0)
            last_pos = self.positions[-1]
            next_pos = self.trajectory(last_pos, self.position, 0)
            return next_pos
        else:
            direction = self.directionVector()
            return (self.position[0]+direction[0], self.position[1]+direction[1])

    def distance(self, otherPosition, position):
        return ((position[0]-otherPosition[0])**2 + (position[1]-otherPosition[1])**2)**0.5

    def __str__(self):
        return "Ball at %d/%d" % self.position


class SimpleHandBallCollection(object):
    def __init__(self):
        self.balls = []
        self.ballcounter = BallCounter()

    def addPositions(self, ball_list=[], args={}):

        # filtered ball positions (no hands), use copy
        ball_list = list(args['only_balls'])

        # try to update balls, remove non-updated balls
        for ball in self.balls:
            ball.updatedAlready = False
            for new_ball in ball_list:
                if ball.isClose(new_ball):
                    ball.updatePosition(new_ball['position'], radius=new_ball['radius'])
                    ball.updatedAlready = True
                    ball_list.remove(new_ball)
            if not ball.updatedAlready:
                self.balls.remove(ball)

        # create new balls at unused positions
        for ball in ball_list:
            self.balls.append(SimpleHandBall(ball['position'], radius=ball['radius']))

        self.ballcounter.update(self.balls)
        args['ballcounter'] = self.ballcounter


class BallCounter(object):
    """docstring for BallCount"""
    def __init__(self):
        self.count = None
        self.last = []
        self.length = 15 # how many frames to analyse

    def update(self, balls):
        self.last.append(len(balls))
        if len(self.last) > self.length:
            self.count = sum(self.last[::-1][:self.length]) / (self.length*1.0)
            self.count = int(math.ceil(self.count)) + 1
