# tmp
import cv
colours = [cv.RGB(0, 0, 255), cv.RGB(0, 255, 0), cv.RGB(255, 0, 0), cv.RGB(0, 255, 255), cv.RGB(255, 0, 255)]
def getcolour():
    try:
        return colours.pop()
    except:
        return cv.RGB(255, 255, 255)


class Ball(object):
    """docstring for Ball"""
    def __init__(self, position, radius=10):
        self.colour = getcolour()
        self.position = position
        self.positions = []
        self.radius = radius
        self.updatedAlready = False
        self.closeThreshold = 35 # pixel distance for 2 balls to be considered "close"

    def updatePosition(self, position, radius=10):
        self.positions.append( self.position )
        self.position = position
        self.updatedAlready = True

    def lastPosition(self, n=1):
        if len(self.positions > (n-1)):
            return self.positions[-n]
        else:
            return self.position

    def isClose(self, otherBall):
        otherPosition = otherBall['position']
        return (self.distance(otherPosition) < self.closeThreshold)

    def distance(self, otherPosition):
        return ((self.position[0]-otherPosition[0])**2 + (self.position[1]-otherPosition[1])**2)**0.5

    def __str__(self):
        return "Ball at %d/%d" % self.position

class BallCollection(object):
    def __init__(self):
        self.balls = []

    def addPositions(self, ball_list=[]):
        # first call?
        if not len(self.balls):
            for ball in ball_list:
                self.balls.append(Ball(ball['position'], radius=ball['radius']))
        else: # find the right ball to update
            for new_ball in ball_list:
                for ball in self.balls:
                    if not ball.updatedAlready and ball.isClose(new_ball):
                        ball.updatePosition(new_ball['position'], radius=new_ball['radius'])
            # reset ball updated status
            for ball in self.balls:
                if not ball.updatedAlready:
                    # fallback update
                    ball.updatePosition(ball.position, ball.radius)
                ball.updatedAlready = False


