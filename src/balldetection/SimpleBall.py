# tmp
import cv
import numpy as np
from src.Util import getcolour
from src.balldetection.Ball import SimpleBall


class SimpleBallFilter(object):
    def __init__(self):
        self.balls = []

    def filter(self, rgb, depth, ball_list, args={}):

        # first call?
        if not len(self.balls):
            if len(ball_list) == 3:
                for ball in ball_list:
                    self.balls.append(SimpleBall(ball['position'], radius=ball['radius']))

        else: # find the right ball to update

            # remember which balls have been updated in this frame
            updated = dict(zip(self.balls, [False for _ in self.balls]))

            # update all balls with "close" positions
            for new_ball in ball_list:
                new_ball['used'] = False
                for ball in self.balls:
                    if not updated[ball] and ball.isClose(new_ball):
                        new_ball['used'] = True
                        ball.updatePosition(new_ball['position'])
                        updated[ball] = True

            # now update the balls that were not "close" using the closest of the remaining positions
            non_updated_balls = [b for b in self.balls if not updated[b]]
            non_used_positions = [p for p in ball_list if not p['used']]
            for ball in non_updated_balls:
                if len(non_used_positions) == 0:
                    return rgb, depth, self.balls
                pos = sorted(non_used_positions, key=lambda p: ball.distance(p['position'], ball.futurePosition(True)))[0]
                ball.updatePosition(pos['position'])
                non_used_positions.remove(pos)

            # reset ball updated status
            for ball in self.balls:
                updated[ball] = False

        return rgb, depth, self.balls
