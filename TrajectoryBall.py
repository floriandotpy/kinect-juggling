from Util import getcolour

class TrajectoryBall(object):
    def __init__(self, lowerPoint, upperPoint, meta=None):
        # remember older positions
        self.positions = []

        # meta data (like rects that created this ball)
        self.meta = meta

        # for drawing
        self.radius = 10
        self.colour = getcolour()

        # gravity, positive because y is upside-down
        self.gravity = 9.81 * 0.5

        self._initTrajectory(lowerPoint, upperPoint)

        # initial position
        self.position = None
        self.step()
        self.firstPosition = self.position

    def _initTrajectory(self, lowerPoint, upperPoint):
        # unpack
        (x1, y1), (x2, y2) = lowerPoint, upperPoint

        # speed in x and y direction
        self.v_x = x2 - x1
        self.v_y = y2 - y1

        # why is the calculated speed too fast? need to correct it here
        # self.v_x *= 0.5
        self.v_y *= 0.8

        # start trajectory in center of the two points we are based on
        self.xOffset = (x2 + x1) / 2
        self.yOffset = (y2 + y1) / 2
        self.xOffset = x1
        self.yOffset = y1

        # progress of the trajectory
        self.t = 0


    def futurePosition(self):
        return self._trajectory(self.t+1)

    def directionVector(self):
        return (0,0)

    def _trajectory(self, t=1):
        """Calculate the throw trajectory based on 2 points
        to return any future or past point on that trajectory"""

        # distance in x and y direction
        x   = self.v_x * t + self.xOffset
        y   = self.v_y * t + self.gravity/2 * t**2 + self.yOffset

        return int(x), int(y)

    def matches(self, position):
        """determine whether the predicted position could match a
        given data point"""

        position = position['position']
        predictedPos = self._trajectory(self.t+1)
        distance_x = abs(predictedPos[0] - position[0])
        distance_y = abs(predictedPos[1] - position[1])
        distance = (distance_x**2 + distance_y**2)**0.5

        return distance < 20

    def update(self, position_raw):
        position = position_raw['position']
        self._initTrajectory(self.position, position)
        self.position = position


    def step(self):
        if self.position:
            self.positions.append(self.position)
        self.position = self._trajectory(self.t)
        self.t += 1


class TrajectoryBallCollection(object):
    def __init__(self):
        self.positions = []
        self.balls = []
        self.lastFrame = []

    def addPositions(self, positions=[], args={}):
        self.lastFrame = positions

        # forget positions that are known to be hands
        positions = args['only_balls']

        # remember last frame before using current frame
        if len(self.lastFrame) == 0:
            self.lastFrame = positions
            return

        # update existing balls if possible
        # for ball in self.balls:
        #     for pos in positions:
        #         if ball.matches(pos):
        #             print "match!"
        #             positions.remove(pos)
        #             ball.update(pos)

        # launch new balls
        for oldPos in self.lastFrame:
            for newPos in positions:
                oldX, oldY = oldPos['position']
                newX, newY = newPos['position']

                isAbove = newY < oldY
                # isAbove = True
                isNotTooHigh = abs(newY - oldY) < 60
                isCloseX = abs(newX - oldX) < 30
                midX = args['centerX'] # FIXME: dynamic calculation (mid point between outermost rects)
                isInward = (oldX < newX and oldX < midX) or (oldX > newX and oldX > midX)

                if isAbove and isCloseX and isNotTooHigh:
                # upwards movement!
                    self.launchTrajectory(oldPos['position'], newPos['position'], meta={'old': oldPos, 'new': newPos})

        # move balls
        self.step()

    def launchTrajectory(self, lowerPoint, upperPoint, meta=None):
        ball = TrajectoryBall(lowerPoint, upperPoint, meta=meta)
        self.balls.append(ball)

    def step(self):
        for ball in self.balls:
            ball.step()
            if ball.t > 25:
                self.balls.remove(ball)
            # if ball.position[1] > 380 or not -200 < ball.position[0] < 840:
            #     self.balls.remove(ball)
