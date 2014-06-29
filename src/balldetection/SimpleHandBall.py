import math
from src.Util import getcolour
from src.balldetection.Ball import SimpleBall


class SimpleHandBallFilter(object):
    def __init__(self):
        self.balls = []

    def filter(self, rgb, depth, ball_positions, args={}):

        # try to update balls from last frame, remove non-updated balls
        for ball in self.balls:

            # remember which balls have been updated in this frame
            updated = dict(zip(self.balls, [False for _ in self.balls]))

            # find match from ball <-> position
            for new_ball in ball_positions:
                if ball.isClose(new_ball, future=False):
                    ball.updatePosition(new_ball['position'])
                    updated[ball] = True
                    ball_positions.remove(new_ball)

            # get rid of balls where we couldn't find a matching position
            if not updated[ball]:
                self.balls.remove(ball)

        # create new balls at unused positions
        for ball in ball_positions:
            self.balls.append(SimpleBall(ball['position'], radius=ball['radius']))

        return rgb, depth, list(self.balls)