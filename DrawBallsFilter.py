import cv
import numpy as np

class DrawBallsFilter(object):

    def filter(self, rgb, depth, args={}):
        rgb_cv = cv.fromarray(np.array(rgb[:,:,::-1]))

        balls = args['balls'].balls
        print "drawing %d balls" % len(balls)
        for ball in balls:
            cv.Circle(rgb_cv, ball.position, ball.radius, ball.colour, thickness=-1, lineType=8, shift=0)

        rgb = np.copy(rgb_cv)[:,:,::-1]

        return rgb, depth
