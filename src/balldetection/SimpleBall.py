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
            print str(len(ball_list)) + " balls"
            if len(ball_list) == 3:
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
                        ball.updatePosition(new_ball['position'])
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

        return rgb, depth, self.balls
