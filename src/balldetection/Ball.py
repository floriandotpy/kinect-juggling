from src.Util import getcolour

class Ball(object):
    def __init__(self, position, radius=10, meta=None, max_history=2):
        """Represents a single ball mid-air, with its positions being updated every frame."""
        self.colour = getcolour()
        self.position = position
        self.radius = radius
        self.meta = meta
        self.positions = [] # collect older positions
        self.max_history = max_history
        self.updatedAlready = False

    def updatePosition(self, position):
        self.positions = self.positions[:self.max_history] # keep positions list short
        self.positions.append(self.position)
        self.position = position
        self.updatedAlready = True

    def futurePosition(self, trajectory=False):
        # this one doesnt to future predction, return current position instead
        return self.position

    def __str__(self):
        return "Ball at %d/%d" % self.position

class SimpleBall(Ball):
    """Represents a single ball mid-air, with its positions being updated every frame."""
    def __init__(self, position, radius=10, meta=None, max_history=10):
        super(SimpleBall, self).__init__(position, radius, meta, max_history)
        self.closeThreshold = 40 # pixel distance for 2 balls to be considered "close"

    def __str__(self):
        return "Ball at %d/%d" % self.position

    def directionVector(self):
        n = 2
        if len(self.positions) < n:
            return (0, 0)
        else:
            last_pos = self.positions[-1]
            x = self.position[0] - last_pos[0]
            y = self.position[1] - last_pos[1]
            return (x, y)

    def trajectory(self, (x1, y1), (x2, y2), t=1):
        """Calculate the throw trajectory based of 2 points return any future
        or past point on that trajectory"""

        # gravity, positive because y is upside-down
        g   = 9.81 * 0.4

        # speed in x and y direction
        v_x = x2 - x1
        v_y = y2 - y1

        # distance in x and y direction
        x   = v_x * t + x2
        y   = v_y * t + g/2 * t**2 + y2

        return int(x), int(y)

    def isClose(self, otherBall, future=True):
        otherPosition = otherBall['position']
        myPosition = self.futurePosition(True) if future else self.position
        return (self.distance(otherPosition, myPosition) < self.closeThreshold)

    def futurePosition(self, trajectory=False):
        if trajectory:
            if len(self.positions) < 2:
                return (0, 0)
            last_pos = self.positions[-1]
            next_pos = self.trajectory(last_pos, self.position, 0)
            return next_pos
        else:
            direction = self.directionVector()
            return (self.position[0]+direction[0], self.position[1]+direction[1])

    def distance(self, otherPosition, position):
        return ((position[0]-otherPosition[0])**2 + (position[1]-otherPosition[1])**2)**0.5

class PreciseTrajectoryBall(Ball):
    def __init__(self, posOne, posTwo, posThree, meta=None, max_history=10):
        super(SimpleBall, self).__init__(position, radius, meta, max_history)

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