import numpy as np
from PIL import Image

import cv
import cv2
import random
import time


import scipy
import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters
# import matplotlib.pyplot as plt

def discoMode(rgb):
    """
        Adds nyan cat mode to your life, therefore enhancing it by factor 1000.
    """
    # Shuffle RGB channels for every pixel
    l = [0, 1, 2]
    random.shuffle(l)
    mapping = ([0, 1, 2], l)
    rgb[:, :, mapping[0][0]], rgb[:, :, mapping[0][1]], rgb[:, :, mapping[0][1]] = \
        rgb[:, :, mapping[1][0]], rgb[:, :, mapping[1][1]], rgb[:, :, mapping[1][2]]
    return rgb

def canny(depth, as_cv=False):
    print "trying canny..."
    img = cv.fromarray(depth, cv.CV_8UC1)
    mat1 = cv.CreateMat(img.rows, img.cols, cv.CV_8UC1)
    mat2 = cv.CreateMat(img.rows, img.cols, cv.CV_8UC1)
    cv.Convert(img, mat1)
    # img2 = cv.CreateMat(img.rows, img.cols, cv.CV_8UC1)
    # print img.rows, img.cols, img2.rows, img2.cols
    # print img.type, img2.type
    cv.Canny(mat1, mat2, 50, 200) # ???
    print "done with canny..."
    if cv:
        return mat2
    return np.asarray(mat2)

def findHoughCircles(rgb):
    # maxd = np.amax(depth)
    # subset = depth >  maxd - 2 * maxd / 3
    # rgb2[subset] = 255
    rgb = np.copy(rgb)
    print rgb.shape

    img = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
    img = cv.fromarray(img)

    cv.Smooth(img, img, cv.CV_GAUSSIAN, 9, 0, 0, 0)

    # canny = cv.CreateImage(cv.GetSize(img), 8, 1)
    # cv.Canny(img, canny, 5, 40)

    height = img.height
    width = img.width
    storage = cv.CreateMat(height, 1, cv.CV_32FC3)
    # HoughCircles(image, circle_storage, method, dp, min_dist [, param1 [, param2 [, min_radius [, max_radius]]]]) -> None
    # cv.fromarray(np.copy(rgb[:,:,0]))
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

def hough(rgb, depth):
    circles = findHoughCircles(rgb)

    for (x,y,r) in circles:
        if (x-r > 0 and x+r < 640 and y-r > 0 and y+r < 460):
            cv.Circle(cv.fromarray(rgb), (int(x),int(y)), int(abs(r)), cv.RGB(0, 0, 255), thickness=-1, lineType=8, shift=0)

    return rgb

def kalman(x, y):
    kalman = cv.CreateKalman(4, 2, 0)
    kalman_state = cv.CreateMat(4, 1, cv.CV_32FC1)
    kalman_process_noise = cv.CreateMat(4, 1, cv.CV_32FC1)
    kalman_measurement = cv.CreateMat(2, 1, cv.CV_32FC1)

    # set previous state for prediction
    kalman.state_pre[0,0]  = x
    kalman.state_pre[1,0]  = y
    kalman.state_pre[2,0]  = 0
    kalman.state_pre[3,0]  = 0

    # set kalman transition matrix
    kalman.transition_matrix[0,0] = 1
    kalman.transition_matrix[0,1] = 0
    kalman.transition_matrix[0,2] = 0
    kalman.transition_matrix[0,3] = 0
    kalman.transition_matrix[1,0] = 0
    kalman.transition_matrix[1,1] = 1
    kalman.transition_matrix[1,2] = 0
    kalman.transition_matrix[1,3] = 0
    kalman.transition_matrix[2,0] = 0
    kalman.transition_matrix[2,1] = 0
    kalman.transition_matrix[2,2] = 0
    kalman.transition_matrix[2,3] = 1
    kalman.transition_matrix[3,0] = 0
    kalman.transition_matrix[3,1] = 0
    kalman.transition_matrix[3,2] = 0
    kalman.transition_matrix[3,3] = 1

    # set Kalman Filter
    cv.SetIdentity(kalman.measurement_matrix, cv.RealScalar(1))
    cv.SetIdentity(kalman.process_noise_cov, cv.RealScalar(1e-5))
    cv.SetIdentity(kalman.measurement_noise_cov, cv.RealScalar(1e-1))
    cv.SetIdentity(kalman.error_cov_post, cv.RealScalar(1))

    kalman_prediction = cv.KalmanPredict(kalman)
    predict_pt  = (kalman_prediction[0,0], kalman_prediction[1,0])

    kalman_estimated = cv.KalmanCorrect(kalman, kalman_measurement)
    state_pt = (kalman_estimated[0,0], kalman_estimated[1,0])

    kalman_measurement[0, 0] = x
    kalman_measurement[1, 0] = y


def parallaxCorrect(depth, x, y):
    """
        Moves the depth field by a given x and y distance.
    """
    depth[y:, :-x] = depth[:-y, x:]
    depth[:, -x:] = True
    depth[:y, :] = True
    return depth

def maxima(rgb, depth):
    # TODO ROLF
    # http://stackoverflow.com/questions/9111711/get-coordinates-of-local-maxima-in-2d-array-above-certain-value
    neighborhood_size = 15
    threshold = 30


    data = depth
    # data = scipy.misc.imread(fname)

    data_max = filters.maximum_filter(data, neighborhood_size)
    maxima = (data == data_max)
    data_min = filters.minimum_filter(data, neighborhood_size)
    diff = ((data_max - data_min) > threshold)
    maxima[diff == 0] = 0

    # cv.Circle(cv.fromarray(rgb), (int(x),int(y)), int(abs(r)), cv.RGB(0, 0, 255), thickness=-1, lineType=8, shift=0)

    # labeled, num_objects = ndimage.label(maxima)
    # slices = ndimage.find_objects(labeled)
    # x, y = [], []
    # for dy,dx in slices:
    #     x_center = (dx.start + dx.stop - 1)/2
    #     x.append(x_center)
    #     y_center = (dy.start + dy.stop - 1)/2
    #     y.append(y_center)

    # print x, y

    # print np.nonzero(maxima)

    rgb[maxima] = [255, 0, 0]

    return cv.fromarray(np.array(rgb[:,:,::-1], dtype=np.uint8))

    # return maxima

class BallDetector(object):
    """docstring for BallDetector """
    def __init__(self, ballcolor, threshold):
        self.ballcolorarray = np.empty(shape=(480, 640, 3), dtype=np.uint8)
        self.ballcolorarray[:, :] = np.array(ballcolor)
        self.ballcolor = ballcolor
        self.threshold = threshold
        self.WIDTH = 640
        self.HEIGHT = 480

    def detectHoles(self, depth):
        white = np.zeros(shape=(480, 640))
        white.fill(0)
        subset_objects = depth < 2100 # chosen by experiment for example frames
        subset_holes = depth == 0
        white[subset_objects] = 2047
        white[subset_holes] = 0
        return white

    def detect(self, rgb):
        b = abs(rgb - self.ballcolorarray) < self.threshold
        b = np.logical_and(np.logical_and(b[:,:,0], b[:,:,1]), b[:,:,2])
        rgb = np.zeros(shape=(480, 640, 3), dtype=np.uint8)
        rgb[b] = np.array([255, 0, 255])
        return rgb

    def detectDepth(self, rgb, depth):
        return rgb

        rgb = np.zeros(shape=(480, 640, 3), dtype=np.uint8)
        subset = depth < 100
        rgb[subset] = self.ballcolor
        return rgb

    def drawRects(self, rgb, depth, draw_here):
        storage = cv.CreateMemStorage(0)
        contour = cv.FindContours(depth, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
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
                #
                x -= 5
                y -= 5
                w += 10
                h += 10
                cv.Rectangle(rgb, (x, y), (x+w, y+h), cv.CV_RGB(0, 255,0), 2)

                circles = findHoughCircles(rgb[y:y+h, x:x+w])
                print "%d circles found" % len(circles)
                if len(circles) > 1:
                    circles = circles[:1] # only the first circle for now
                for circle_x, circle_y, r in circles:
                    if 0 < circle_x-r and circle_x+r < w and 0 < circle_y-r and circle_y+r<h:
                        cv.Circle(rgb, (x+int(circle_x), int(y+circle_y)), int(r), cv.RGB(0, 0, 255), thickness=-1, lineType=8, shift=0)
        f = cv.InitFont(cv.CV_FONT_HERSHEY_PLAIN, 1.0, 1.0)
        # PutText(img, text, org, font, color)
        cv.PutText(rgb, 'Rects:', (20, 20), f, (255, 255, 255))
        cv.PutText(rgb, str(rectcount), (50 + rectcount * 15, 20), f, (0, 0, 0))


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


