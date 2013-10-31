class NoFilter(object):

    def __init__(self):
        pass

    def filter(self, rgb, depth, args = {}):
        return rgb, depth