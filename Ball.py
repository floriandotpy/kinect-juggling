class Ball(object):
    """docstring for Ball"""
    def __init__(self, position):
        self.position = position
        self.positions = []
        self.updatedAlready = False
        self.closeThreshold = 50 # pixel distance for 2 balls to be considered "close"

    def updatePosition(self, position):
        self.positions.append( self.position )
        self.position = position
        self.updatedAlready = True

    def lastPosition(self, n=1):
        if len(self.positions > (n-1)):
            return self.positions[-n]
        else:
            return self.position

    def isClose(self, otherPosition):
        return (self.distance(otherPosition) < self.closeThreshold)

    def distance(self, otherPosition):
        return ((self.position[0]-otherPosition[0])**2 + (self.position[1]-otherPosition[1])**2)**0.5

    def __str__(self):
        return "Ball at %d/%d" % self.position

class BallCollection(object):
    def __init__(self):
        self.balls = []

    def addPositions(self, positions=[]):
        # first call?
        if not len(self.balls):
            for pos in positions:
                self.balls.append(Ball(pos))
        else: # find the right ball to update
            for pos in positions:
                for ball in self.balls:
                    if not ball.updatedAlready and ball.isClose(pos):
                        ball.updatePosition(pos)
            # reset ball updated status
            for ball in self.balls:
                if not ball.updatedAlready:
                    # fallback update
                    ball.updatePosition(ball.position)
                ball.updatedAlready = False

            print self.balls[-1]

