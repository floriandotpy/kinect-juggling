import numpy as np

class CutOffFilter(object):

    def filter(self, rgb, depth, balls, args = {}):
        white = np.zeros(shape=(480, 640), dtype=np.uint8)
        white.fill(0)
        subset_objects = (depth < 2100) # chosen by experiment for example frames
        subset_holes = (depth == 0)
        white[subset_objects] = 4095
        white[subset_holes] = 0

        return rgb, white, balls