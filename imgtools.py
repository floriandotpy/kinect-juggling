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

    def drawRects(self, rgb, depth):

        # find rectangles
        x,y,w,h = cv2.boundingRect(contours)

        # draw rectangles
        cv2.rectangle(rgb,(x,y),(x+w,y+h),(0,255,0),2)

        # approx = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(contours,True),True)
        return rgb

    def drawRects2(self, rgb, depth, draw_here):
        storage = cv.CreateMemStorage(0)
        contour = cv.FindContours(depth, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
        points = []

        while contour:
            x,y,w,h = cv.BoundingRect(list(contour))
            contour = contour.h_next()

            # filter out small and border touching rectangles
            t = 2 # tolerance threshold
            minsize = 5
            if x > t and y > t and x+w < self.WIDTH - t and y+h < self.HEIGHT - t and w > minsize and h > minsize:
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
    """Offers access to rgb and depth from the real Kinect"""
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

