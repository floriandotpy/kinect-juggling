class Hand(object):
    """A hand of the juggler"""
    def __init__(self, position):

        # unpack position
        self.x, self.y = position

        # rememeber past positions
        self.positions = []

    def update(self, newPosition):
        self.last = (self.x, self.y)
        self.x, self.y = newPosition

    def isClose(self, otherPosition):
        otherX, otherY = otherPosition
        threshold = 50
        isCloseX = abs(self.x - otherX) < threshold
        isCloseY = abs(self.y - otherY) < threshold
        return isCloseX and isCloseY

class HandCollection(object):
    def __init__(self):
        self.left = Hand((100, 100))
        self.right = Hand((200, 200))
        self.isFirstStep = True

    def addPositions(self, ball_positions):
        positions = [b['position'] for b in ball_positions]
        centerX = 360

        allLeft = filter(lambda p: p[0] <= centerX, positions)
        if len(allLeft) > 0:
            lowestLeft = sorted(allLeft, key=lambda p: -1*p[1])[0]
            if self.isFirstStep or self.left.isClose(lowestLeft):
                self.left.update(lowestLeft)

        allRight = filter(lambda p: p[0] > centerX, positions)
        if len(allRight) > 0:
            lowestRight = sorted(allRight, key=lambda p: -1*p[1])[0]
            if self.isFirstStep or self.right.isClose(lowestRight):
                self.right.update(lowestRight)

        self.isFirstStep = False
