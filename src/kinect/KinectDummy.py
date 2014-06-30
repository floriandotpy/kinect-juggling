import os
import numpy as np

class KinectDummy(object):
    """Offers access to recorded dummy data the same way the Kinect would return it"""
    def __init__(self):
        self.path = "frames"
        (_, _, files) = os.walk(self.path).next()
        self.frames_rgb = []
        self.frames_depth = []
        for filename in files:
            if "rgb" in filename:
                self.frames_rgb.append(filename)
            elif "depth" in filename:
                self.frames_depth.append(filename)
        self.frames_rgb = sorted(self.frames_rgb)
        self.frames_depth = sorted(self.frames_depth)

        self.current = 0
        self.total = len(self.frames_rgb)

    def get_frame(self, record=False):
        rgb = np.load(os.path.join(self.path,self.frames_rgb[self.current]))
        depth = np.load(os.path.join(self.path,self.frames_depth[self.current]))
        self.current = (self.current + 1) % self.total
        return (rgb, depth)

    def snapshot(self):
        pass