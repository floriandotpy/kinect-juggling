import cv
import numpy as np

class DrawBallsFilter(object):

    def __init__(self):
        self.font = cv.InitFont(cv.CV_FONT_HERSHEY_PLAIN, 1.0, 1.0)


    def filter(self, rgb, depth, args={}):
        rgb_cv = cv.fromarray(np.array(rgb[:,:,::-1]))

        balls = args['balls'].balls
        for ball in balls:
            cv.Circle(rgb_cv, ball.position, ball.radius, ball.colour, thickness=-1, lineType=8, shift=0)
            cv.PutText(rgb_cv, '%d/%d' % ball.position, ball.position , self.font, (255, 255, 255))


        rgb = np.copy(rgb_cv)[:,:,::-1]

        return rgb, depth
