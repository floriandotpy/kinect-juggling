import numpy as np
import cv
import cv2

class RectsFilter(object):

    def __init__(self):

        # FIXME: this has to go somewhere else...
        self.WIDTH = 640
        self.HEIGHT = 480

        self.font = cv.InitFont(cv.CV_FONT_HERSHEY_PLAIN, 1.0, 1.0)


    def _nullify(self, i):
        return i if i > 0 else 0

    def filter(self, rgb, depth, args = {}):

        # custom depth input (from CutOffFilter)
        # I think this is so that we do not destroy the original depth. rubbish?
        if 'depth_out' in args:
            my_depth = args['depth_out']

        # We'll need open CV for this.
        rgb_cv = cv.fromarray(np.array(rgb[:,:,::-1]))
        depth_cv = cv.fromarray(np.array(my_depth[:,:], dtype=np.uint8))

        storage = cv.CreateMemStorage(0)
        contour = cv.FindContours(depth_cv, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
        points = []

        ball_list = [] # collect ballpositions in loop
        while contour:
            x,y,w,h = cv.BoundingRect(list(contour))
            contour = contour.h_next()

            # filter out small and border touching rectangles
            t = 2 # tolerance threshold
            minsize = 5
            if x > t and y > t and x+w < self.WIDTH - t and y+h < self.HEIGHT - t and w > minsize and h > minsize:
                x -= 5
                y -= 5
                w += 10
                h += 10
                x, y = self._nullify(x), self._nullify(y) # why is this necessary now?

                ball_center = (x+w/2, y+h/2)
                ball_radius = min(w/2, h/2)
                ball_list.append(dict(position=ball_center, radius=ball_radius))

                # Draw rectancle with info
                cv.PutText(rgb_cv, '%d/%d' % (x, y), (x,y-2) , self.font, (0, 255, 0))
                cv.Rectangle(rgb_cv, (x, y), (x+w, y+h), cv.CV_RGB(0, 255,0), 2)

        # update hands, remember the unused positions
        args['only_balls'] = args['hands'].addPositions(ball_list, args)
        args['balls'].addPositions(ball_list, args)

        # and back to numpy with this...
        rgb = np.copy(rgb_cv)[:,:,::-1]

        return rgb, depth

    def findHoughCircles(self, rgb):
        rgb = np.copy(rgb)

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