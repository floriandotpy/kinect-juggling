import cv
import numpy as np

class DrawBallsFilter(object):

    def __init__(self):
        self.font = cv.InitFont(cv.CV_FONT_HERSHEY_PLAIN, 1.0, 1.0)


    def filter(self, rgb, depth, args={}):
        rgb_cv = cv.fromarray(np.array(rgb[:,:,::-1]))

        # draw line (center of juggling pattern)
        centerX = args['centerX']
        cv.Line(rgb_cv, (centerX, 0), (centerX, 480), (200,200,200), thickness=2, lineType=8, shift=0)


        # draw hands
        if 'hands' in args:
            leftHand = args['hands'].left
            rightHand = args['hands'].right
            for hand in (leftHand, rightHand):
                cv.Circle(rgb_cv, (hand.x, hand.y), 15, (128, 255, 255), thickness=-1, lineType=8, shift=0)


        # draw balls
        balls = args['balls'].balls
        for ball in balls:
            cv.Circle(rgb_cv, ball.position, ball.radius, ball.colour, thickness=-1, lineType=8, shift=0)
            # highlight rects that this ball is based upon
            if ball.meta:
                for r in [ball.meta['old'], ball.meta['new']]:
                    radius = r['radius']
                    top_left = (r['position'][0]-radius/2, r['position'][1]-radius/2)
                    bottom_right = (r['position'][0]+radius/2, r['position'][1]+radius/2)
                    cv.Rectangle(rgb_cv, top_left, bottom_right, ball.colour, 2)


            # cv.Circle(rgb_cv, ball.firstPosition, int(ball.radius*1.5), ball.colour, thickness=-1, lineType=8, shift=0)
            # cv.Circle(rgb_cv, ball.futurePosition(), ball.radius, ball.colour, thickness=-1, lineType=8, shift=0)
            cv.PutText(rgb_cv, '%d/%d' % ball.position, ball.position , self.font, (255, 255, 255))
            prevPos = ball.position
            thickness = 6
            for olderPosition in ball.positions[::-1]:
                cv.Line(rgb_cv, prevPos, olderPosition, ball.colour, thickness=thickness, lineType=8, shift=0)
                thickness = max(abs(thickness - 1), 1)
                prevPos = olderPosition


            # direction = ball.directionVector()
            # cv.Line(rgb_cv, ball.position, (ball.position[0]-direction[0], ball.position[1]-direction[1]), ball.colour, thickness=3, lineType=8, shift=0)

        rgb = np.copy(rgb_cv)[:,:,::-1]

        return rgb, depth
