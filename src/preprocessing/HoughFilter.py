import numpy as np
import cv, cv2
import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters

class HoughFilter(object):

    def findHoughCirclesfromRGB(self, rgb):
        img = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
        return self.findHoughCircles(img)

    def findHoughCircles(self, img):
        img = cv.fromarray(img)

        cv.Smooth(img, img, cv.CV_GAUSSIAN, 9, 0, 0, 0)

        height = img.height
        width = img.width
        storage = cv.CreateMat(height, 1, cv.CV_32FC3)
        try:
            cv.HoughCircles(img, storage, cv.CV_HOUGH_GRADIENT,
                dp=1, min_dist=10, param1=2,
                param2=10, min_radius=5, max_radius=40)
        except:
            print "LOLWUT?"
            return []

        circles = []
        for i in xrange(storage.rows):
            (x,y,r) = storage[i,0]
            circles.append( (x, y, r) )

        return circles

    def filter(self, rgb, depth, argv = {}):
        # circles = self.findHoughCircles(depth)
        circles = self.findHoughCirclesfromRGB(rgb)

        print circles

        for (x,y,r) in circles:
            if (x-r > 0 and x+r < 640 and y-r > 0 and y+r < 460):
                cv.Circle(cv.fromarray(rgb), (int(x),int(y)), int(abs(r)), cv.RGB(0, 0, 255), thickness=-1, lineType=8, shift=0)

        return rgb, depth