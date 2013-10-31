import random

"""
    Adds nyan cat mode to your life, therefore enhancing it by factor 1000.
"""
class DiscoFilter(object):

    def filter(self, rgb, depth, args = {}):

        # Shuffle RGB channels for every pixel
        l = [0, 1, 2]
        random.shuffle(l)
        mapping = ([0, 1, 2], l)
        rgb[:, :, mapping[0][0]], rgb[:, :, mapping[0][1]], rgb[:, :, mapping[0][1]] = \
            rgb[:, :, mapping[1][0]], rgb[:, :, mapping[1][1]], rgb[:, :, mapping[1][2]]
        return rgb, depth