import math
from src.Util import getcolour
from src.balldetection.Ball import SimpleBall


class SimpleHandBallFilter(object):
    def __init__(self):
        self.balls = []

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


        return rgb, depth, list(self.balls)

