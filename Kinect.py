from freenect import sync_get_depth as get_depth, sync_get_video as get_video

class Kinect(object):
    """Offers access to rgb and depth from the real Kinect"""
    def __init__(self):
        pass

    def get_frame(self):
        # Get a fresh frame
        (depth,_) = get_depth(format=4)
        (rgb,_) = get_video()
        return (rgb, depth)