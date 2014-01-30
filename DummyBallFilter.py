import cv
import numpy as np
from DummyBall import DummyBall

class DummyBallFilter(object):

    def __init__(self):
        ball = DummyBall()
        self.balls = [ball]
        self.font = cv.InitFont(cv.CV_FONT_HERSHEY_PLAIN, 1.0, 1.0)

    def filter(self, rgb, depth, args={}):
        rgb_cv = cv.fromarray(np.array(rgb[:,:,::-1]))

        for ball in self.balls:
            cv.Circle(rgb_cv, ball.position, ball.radius, cv.RGB(255, 255, 255), thickness=-1, lineType=8, shift=0)
            cv.PutText(rgb_cv, '%d/%d' % ball.position, ball.position , self.font, (255, 255, 255))
            # direction = ball.directionVector()
            # cv.Line(rgb_cv, ball.position, (ball.position[0]-direction[0], ball.position[1]-direction[1]), cv.RGB(255, 255, 255), thickness=3, lineType=8, shift=0)

        rgb = np.copy(rgb_cv)[:,:,::-1]

        return rgb, depth
