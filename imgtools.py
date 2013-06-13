import numpy as np
from PIL import Image
import os
import cv
import cv2
import random
import time
from freenect import sync_get_depth as get_depth, sync_get_video as get_video


def replaceBackground(rgb, depth, background_src, depth_threshold=100):
    """
        Cuts of the rgb image at a given depth and places it on top of
        a background image.
    """
    # load background image
    img = np.asarray(Image.open(background_src))
            # Remove the background based on the depth field
    subset = depth > depth_threshold
    rgb[subset] = img[subset]
    return rgb


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


def parallaxCorrect(depth, x, y):
    """
        Moves the depth field by a given x and y distance.
    """
    depth[y:, :-x] = depth[:-y, x:]
    depth[:, -x:] = True
    depth[:y, :] = True
    return depth

def saveImg(rgb, filename):
    img = Image.fromarray(rgb)
    img.save(filename, "PNG")

def snapshot(rgb, depth):
    filename = "frames/frame-%d" % int(time.time()*1000)
    filename_rgb = filename + "-rgb"
    filename_depth = filename + "-depth"
    np.save(filename_rgb, rgb)
    np.save(filename_depth, depth)
    # imgtools.saveImg(rgb, filename)

def getDummyImg(filename):
    img = np.asarray(Image.open(filename))
    return (img, None)

def detectHoles(depth):
    white = np.zeros(shape=(480, 640))
    white.fill(0)

    subset_objects = depth < 1500
    subset_holes = depth == 0
    white[subset_objects] = 1023
    white[subset_holes] = 100
    return white


class BallDetector(object):
    """docstring for BallDetector """
    def __init__(self, ballcolor, threshold):
        self.ballcolorarray = np.empty(shape=(480, 640, 3), dtype=np.uint8)
        self.ballcolorarray[:, :] = np.array(ballcolor)
        self.ballcolor = ballcolor
        self.threshold = threshold

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

    def drawRects(self, rgb, depth):
        # img = cv.fromarray(depth, cv.CV_8UC1)
        # ret, thresh = cv2.threshold(depth, 127, 255, 0)
        contours, hierarchy = cv2.findContours(depth, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        # find rectangles
        x,y,w,h = cv2.boundingRect(contours)

        # draw rectangles
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

        # approx = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(contours,True),True)
        return img




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

class Kinect(object):
    """Offers acces to rgb and depth from the real Kinect"""
    def __init__(self):
        pass

    def get_frame(self):
        # Get a fresh frame
        (depth,_) = get_depth(format=4)
        (rgb,_) = get_video()
        return (rgb, depth)

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

    def get_frame(self):
        rgb = np.load(os.path.join(self.path,self.frames_rgb[self.current]))
        depth = np.load(os.path.join(self.path,self.frames_depth[self.current]))
        self.current = (self.current + 1) % self.total
        return (rgb, depth)

