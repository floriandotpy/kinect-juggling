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


