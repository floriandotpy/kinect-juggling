import numpy as np
import warnings
from Util import getcolour

# mute that one annoying warning
warnings.simplefilter('ignore', np.RankWarning)


class PreciseTrajectoryBall(object):
    def __init__(self, posOne, posTwo, posThree, meta=None):

        # remember older positions
        self.positions = []

        # meta data (like rects that created this ball)
        self.meta = meta

        # for drawing
        self.radius = 10
        self.colour = getcolour()

        # gravity, positive because y is upside-down
        self.gravity = 9.81 * 0.5

        self._initTrajectory(posOne, posTwo, posThree)

        # initial position
        self.position = None
        self.step()
        self.firstPosition = self.position

    def _initTrajectory(self, posOne, posTwo, posThree):
        xList = [pos[0] for pos in [posOne, posTwo, posThree]]
        yList = [pos[1] for pos in [posOne, posTwo, posThree]]

        # does x fit a linear function?
        self.xMovement = np.polyfit([-2, -1, 0], xList, 1)

        # does y fit a square function?
        self.yMovement = np.polyfit([-2, -1, 0], yList, 2)

        # progress of the trajectory
        self.t = 0

    def futurePosition(self):
        return self._trajectory(self.t+1)

    def directionVector(self):
        return (0,0)

    def _trajectory(self, t=1):
        """Calculate the throw trajectory"""

        # distance in x and y direction
        x   = np.polyval(self.xMovement, t)
        # y   = self.v_y * t + self.gravity/2 * t**2 + self.yOffset
        y   = np.polyval(self.yMovement, t)

        return int(x), int(y)

    def matches(self, position):
        """determine whether the predicted position could match a
        given data point"""

        return False

    def update(self, position_raw):
        position = position_raw['position']
        self._initTrajectory(self.position, position)
        self.position = position


    def step(self):
        if self.position:
            self.positions.append(self.position)
        self.position = self._trajectory(self.t)
        self.t += 1


class PreciseTrajectoryBallCollection(object):
    def __init__(self):
        self.positions = []
        self.balls = []
        # self.frameQueue = FrameQueue(length=10)
        self.lastFrame = []
        self.frames = [] # remember old frames

    def addPositions(self, positions=[], args={}):

        # remember up to 10 frames, keep order
        if len(self.frames) >= 10:
            self.frames = self.frames[:-10:-1][::-1]
        self.frames.append(positions)

        # we need at least the last 3 frames
        if len(self.frames) < 3:
            return


        for frameOne in self.frames[-2]:
            if frameOne['radius'] > 20:
                continue
            for frameTwo in self.frames[-1]:
                for frameThree in self.frames[0]:
                    posOne, posTwo, posThree = frameOne['position'], frameTwo['position'], frameThree['position']

                    # remember: y is upside down
                    isRising = posOne[1] > posTwo[1] > posThree[1]

                    # shalalala
                    leftMovement  = posOne[0] > posTwo[0] > posThree[0]
                    rightMovement = posOne[0] < posTwo[0] < posThree[0]
                    oneDirection = leftMovement or rightMovement

                    if isRising and oneDirection:
                        self.maybeLaunchBall(posOne, posTwo, posThree)

        # move balls
        self.step()

    def maybeLaunchBall(self, posOne, posTwo, posThree):
        ball = PreciseTrajectoryBall(posOne, posTwo, posThree)
        self.balls.append(ball)

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
