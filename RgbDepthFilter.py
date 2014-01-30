import numpy as np




class RgbDepthFilter(object):
    """Returns the depth as the rgb value so that depth can be visualised."""

    def filter(self, rgb, depth, argv = {}):
        depth = depth/32
        rgb[:,:,0] = depth
        rgb[:,:,1] = depth
        rgb[:,:,2] = depth

        return rgb, depth