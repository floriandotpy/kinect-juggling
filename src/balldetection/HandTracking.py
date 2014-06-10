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

    def addPositions(self, ball_positions, args):
        # use a copy
        positions = list(ball_positions)

        # determine center of juggling pattern
        if len(positions) > 0:
            centerX = sum([b['position'][0] for b in positions]) / len(positions)
        else:
            centerX = 320
        args['centerX'] = centerX

        handProps = [(self.left, lambda p: p['position'][0] <= centerX),
            (self.right, lambda p: p['position'][0] > centerX)]

        for hand, filterKey in handProps:
            # filter in right and left positions
            filtered = filter(filterKey, positions)
            if len(filtered) > 0:
                lowest = sorted(filtered, key=lambda p: -1*p['position'][1])[0]
                lowestPosition = lowest['position']
                # if self.isFirstStep or hand.isClose(lowestPosition):

                hand.update(lowestPosition)
                positions.remove(lowest)

        self.isFirstStep = False

        # return without the positions used to update the hands
        return positions


