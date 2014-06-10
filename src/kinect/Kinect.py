import time
import numpy as np
from freenect import sync_get_depth as get_depth, sync_get_video as get_video

class Kinect(object):
    """Offers access to rgb and depth from the real Kinect"""
    def __init__(self):
        pass

    def get_frame(self, record=False):
        # Get a fresh frame
        (depth,_) = get_depth(format=4)
        (rgb,_) = get_video()
        if record:
            self.snapshot(rgb, depth)
        return (rgb, depth)

    def snapshot(self, rgb, depth):
        filename = "frames_new/frame-%d" % int(time.time()*1000)
        filename_rgb = filename + "-rgb"
        filename_depth = filename + "-depth"
        np.save(filename_rgb, rgb)
        np.save(filename_depth, depth)