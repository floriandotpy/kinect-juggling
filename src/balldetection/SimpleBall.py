# tmp
import cv
import numpy as np
from src.Util import getcolour


class SimpleBall(object):
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


class SimpleBallCollection(object):
    def __init__(self):
        self.balls = []

    def addPositions(self, ball_list=[], args={}):
        # if (len(ball_list) > 3):
        #     # while (len(ball_list) > 3):
        #     #     tmp_list = sorted(ball_list, key=lambda b: -1*(b['position'][0]+b['position'][1]))
        #     #     ball_list = tmp_list[:3]
        #     # return
        #     # calculate center of gravity (=centroid)
        #     positions = [list(b['position']) for b in ball_list]
        #     centroid = map(lambda b: b/float(len(ball_list)), reduce(lambda s, pos: [s[0]+pos[0], s[1]+pos[1]], positions, [0, 0]))
        #     # centroid = (300, 300) # center of body
        #     for ball in ball_list:
        #         ball['distanceToCentroid'] = (abs(ball['position'][0] - centroid[0]) + abs(ball['position'][1] - centroid[1])) / 2
        #     ball_list.sort(key=lambda b: b['position'][1])
        #     ball_list = ball_list[:3]
        # elif len(ball_list) < 3:
        #     # cannot handle less than 3 objects right now
        #     return

        # first call?
        if not len(self.balls):
            print str(len(ball_list)) + " balls"
            if len(ball_list) != 3:
                return
            for ball in ball_list:
                self.balls.append(SimpleBall(ball['position'], radius=ball['radius']))
            print str(len(self.balls)) + " balls"
        else: # find the right ball to update

            # more sophisticated ball updating below:
            for new_ball in ball_list:
                new_ball['used'] = False
                for ball in self.balls:
                    if not ball.updatedAlready and ball.isClose(new_ball):
                        new_ball['used'] = True
                        ball.updatePosition(new_ball['position'], radius=new_ball['radius'])
            # now update the balls that were not "close"
            non_updated_balls = [b for b in self.balls if not b.updatedAlready]
            non_used_positions = [p for p in ball_list if not p['used']]
            for ball in non_updated_balls:
                if len(non_used_positions) == 0:
                    return
                print non_used_positions
                pos = sorted(non_used_positions, key=lambda p: ball.distance(p['position'], ball.futurePosition(True)))[0]
                ball.updatePosition(pos['position'])
                non_used_positions.remove(pos)
            # reset ball updated status
            for ball in self.balls:
                if not ball.updatedAlready:
                    # fallback update
                    ball.updatePosition(ball.position, ball.radius)
                ball.updatedAlready = False

