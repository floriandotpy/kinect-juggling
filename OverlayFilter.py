import numpy as np
import cv

class OverlayFilter(object):

    def __init__(self):
        self.font = cv.InitFont(cv.CV_FONT_HERSHEY_PLAIN, 1.0, 1.0)

    def filter(self, rgb, depth, args = {}):

        color = rgb[240, 320]

        for x in range(0,3):
            for y in range(0,3):
                if x != 1 and y != 1:
                    rgb[239+y, 319+x] = np.array([255,255,255])

        img = cv.fromarray(np.array(rgb[:,:,::-1], dtype=np.uint8))
        cv.PutText(img, 'Color: %s' % (color), (20,20) , self.font, (int(color[2]), int(color[1]), int(color[0])))

        return np.copy(img)[:,:,::-1], depth