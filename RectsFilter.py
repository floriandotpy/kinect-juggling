import numpy as np
import cv
import cv2

class RectsFilter(object):

    def __init__(self):

        # FIXME: this has to go somewhere else...
        self.WIDTH = 640
        self.HEIGHT = 480

    def filter(self, rgb, depth, args = {}):

        # We'll need open CV for this.
        rgb_cv = cv.fromarray(np.array(rgb[:,:,::-1]))
        depth_cv = cv.fromarray(np.array(depth[:,:], dtype=np.uint8))

        storage = cv.CreateMemStorage(0)
        contour = cv.FindContours(depth_cv, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
        points = []

        rectcount = 0
        while contour:
            x,y,w,h = cv.BoundingRect(list(contour))
            contour = contour.h_next()

            # filter out small and border touching rectangles
            t = 2 # tolerance threshold
            minsize = 5
            if x > t and y > t and x+w < self.WIDTH - t and y+h < self.HEIGHT - t and w > minsize and h > minsize:
                rectcount += 1
                # draw rect
                x -= 5
                y -= 5
                w += 10
                h += 10
                cv.Rectangle(rgb_cv, (x, y), (x+w, y+h), cv.CV_RGB(0, 255,0), 2)

                circles = self.findHoughCircles(rgb_cv[y:y+h, x:x+w])
                if len(circles) > 1:
                    circles = circles[:1] # only the first circle for now
                for circle_x, circle_y, r in circles:
                    if 0 < circle_x-r and circle_x+r < w and 0 < circle_y-r and circle_y+r<h:
                        cv.Circle(rgb_cv, (x+int(circle_x), int(y+circle_y)), int(r), cv.RGB(0, 0, 255), thickness=-1, lineType=8, shift=0)
        f = cv.InitFont(cv.CV_FONT_HERSHEY_PLAIN, 1.0, 1.0)
        cv.PutText(rgb_cv, 'Rects:', (20, 20), f, (255, 255, 255))
        cv.PutText(rgb_cv, str(rectcount), (50 + rectcount * 15, 20), f, (0, 0, 0))

        # and back to numpy with this...
        rgb = np.copy(rgb_cv)[:,:,::-1]

        return rgb, depth

    def findHoughCircles(self, rgb):
        rgb = np.copy(rgb)
        print rgb.shape

        img = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
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