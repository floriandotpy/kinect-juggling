class DepthHolesFilter(object):

    def __init__(self, threshold=10):
        self.threshold = threshold;

    def filter(self, rgb, depth, args = {}):

        shadow = (depth <= self.threshold)
        depth[shadow] = 2047

        return rgb, depth