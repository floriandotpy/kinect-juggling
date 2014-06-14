import math
from src.Util import getcolour
from src.balldetection.Ball import SimpleBall


class SimpleHandBallFilter(object):
    def __init__(self):
        self.balls = []
        self.ballcounter = BallCounter()

    def filter(self, rgb, depth, ball_list, args={}):

        # filtered ball positions (no hands), use copy
        ball_list = list(ball_list)

        # try to update balls, remove non-updated balls
        for ball in self.balls:

            # TODO: do not store this at the ball object.
            # use dict instead: updated[ball_instance] = False
            ball.updatedAlready = False

            for new_ball in ball_list:
                if ball.isClose(new_ball, future=False):
                    ball.updatePosition(new_ball['position'])
                    ball.updatedAlready = True
                    ball_list.remove(new_ball)

            if not ball.updatedAlready:
                self.balls.remove(ball)

        # create new balls at unused positions
        for ball in ball_list:
            self.balls.append(SimpleBall(ball['position'], radius=ball['radius']))

        self.ballcounter.update(self.balls)
        args['ballcounter'] = self.ballcounter

        return rgb, depth, list(self.balls)


"""
    A first application example. TODO: move this to src.application package
"""

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
