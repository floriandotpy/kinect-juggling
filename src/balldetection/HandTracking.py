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

class HandTrackingFilter(object):
    def __init__(self):
        self.left = Hand((100, 100))
        self.right = Hand((200, 200))

    def filter(self, rgb, depth, positions, args):
        args['hands'] = True
        args['hand_left'] = self.left
        args['hand_right'] = self.right

        # determine center of juggling pattern
        if len(positions) > 0:
            centerX = sum([b['position'][0] for b in positions]) / len(positions)
        else:
            centerX = 320
        args['centerX'] = centerX

        # two properties for match each hand (left & right)
        handProps = [(self.left, lambda p: p['position'][0] <= centerX),
            (self.right, lambda p: p['position'][0] > centerX)]

        for hand, filterKey in handProps:
            # filter in right and left positions
            filtered = filter(filterKey, positions)
            if len(filtered) > 0:
                lowest = sorted(filtered, key=lambda p: -1*p['position'][1])[0]
                lowestPosition = lowest['position']

                hand.update(lowestPosition)
                positions.remove(lowest)

        # return without the positions used to update the hands
        return rgb, depth, positions


