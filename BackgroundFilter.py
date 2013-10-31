import numpy as np
from PIL import Image

"""
    Cuts of the rgb image at a given depth and places it on top of
    a background image.
"""
class BackgroundFilter(object):

    def __init__(self, background_src, depth_threshold=100):

        self.threshold = depth_threshold

        # load background image
        self.img = np.asarray(Image.open(background_src))

    def step(self, rgb, depth, args = {}):

        # Remove the background based on the depth field
        subset = depth > self.threshold
        rgb[subset] = self.img[subset]

        return rgb, depth
