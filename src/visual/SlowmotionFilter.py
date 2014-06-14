import time

class SlowmotionFilter(object):

    def __init__(self, delay):
        self.delay = delay


    def filter(self, rgb, depth, balls, args={}):
        time.sleep(self.delay)

        return rgb, depth, balls
