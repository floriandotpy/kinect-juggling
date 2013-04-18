import numpy as np
from PIL import Image
import random


def replaceBackground(rgb, depth, background_src, depth_threshold=100):
    """
        Cuts of the rgb image at a given depth and places it on top of
        a background image.
    """
    # load background image
    img = np.asarray(Image.open(background_src))
            # Remove the background based on the depth field
    subset = depth > depth_threshold
    rgb[subset] = img[subset]
    return rgb


def discoMode(rgb):
    """
        Adds nyan cat mode to your life, therefor enhancing it by factor 1000.
    """
    # Shuffle RGB channels for every pixel
    l = [0, 1, 2]
    random.shuffle(l)
    mapping = ([0, 1, 2], l)
    rgb[:, :, mapping[0][0]], rgb[:, :, mapping[0][1]], rgb[:, :, mapping[0][1]] = \
        rgb[:, :, mapping[1][0]], rgb[:, :, mapping[1][1]], rgb[:, :, mapping[1][2]]
    return rgb


def parallaxCorrect(depth, x, y):
    """
        Moves the depth field by a given x and y distance.
    """
    depth[y:, :-x] = depth[:-y, x:]
    depth[:, -x:] = True
    depth[:y, :] = True
    return depth


class SmoothBuffer(object):
    """Reduces noise on the depth image. """
    def __init__(self, buffersize=3):
        self.buffersize = buffersize
        self.buffers = [None for _ in xrange(buffersize)]
        self.buffers_weights = np.array(range(buffersize))
        self.weight_sum = sum(self.buffers_weights) + self.buffersize
        self.buffer_i = 0

    def add(self, depth):
        """ Add a depth image to the buffer """
        self.buffers[self.buffer_i] = depth
        self.buffers_weights = (self.buffers_weights - 1) % self.buffersize
        self.buffer_i = (self.buffer_i + 1) % self.buffersize

    def get(self):
        """ Returns a smoothened depth image """
        if None not in self.buffers:
            depth = self.buffers[-1] * (self.buffers_weights[-1] + 1)
            for i in xrange(self.buffersize-1):
                depth += self.buffers[i] * (self.buffers_weights[i] + 1)
            depth = depth / self.weight_sum
        else:
            depth = self.buffers[self.buffer_i-1]
        return depth
