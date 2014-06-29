import math
from src.Util import getcolour


class TrajectoryBallFilter(object):
    def __init__(self):
        self.balls = []
        self.previousFrame = []

    def filter(self, rgb, depth, ball_positions, args={}):

        # forget positions that are known to be hands (if detected before)
        if 'only_balls' in args:
            ball_positions = args['only_balls']

        # only run filter if we know previous frame's positions
        if len(self.previousFrame) == 0:
            self.previousFrame = ball_positions
            rgb, depth, ball_positions

        # launch new balls
        for oldPos in self.previousFrame:
            for newPos in ball_positions:
                oldX, oldY = oldPos['position']
                newX, newY = newPos['position']

                isAbove = newY < oldY
                isNotTooHigh = abs(newY - oldY) < 60
                isCloseX = abs(newX - oldX) < 30

                if isAbove and isCloseX and isNotTooHigh:
                    # upwards movement!
                    self.launchTrajectory(oldPos['position'], newPos['position'], meta={'old': oldPos, 'new': newPos})

        # move balls
        self.step()

        # remember positions for next frame
        self.previousFrame = ball_positions

        return rgb, depth, list(self.balls)

    def launchTrajectory(self, lowerPoint, upperPoint, meta=None):
        ball = TrajectoryBall(lowerPoint, upperPoint, meta=meta)
        self.balls.append(ball)

    def step(self):
        for ball in self.balls:
            ball.step()
            if ball.t > 15:
                self.balls.remove(ball)


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

        # start trajectory at first point we're based on
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

    def step(self):
        if self.position:
            self.positions.append(self.position)
        self.position = self._trajectory(self.t)
        self.t += 1


