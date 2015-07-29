from primesense import openni2
from primesense import _openni2 as c_api
import numpy as np
import matplotlib.pyplot as plt
import cv

class Gestures(object):
    """docstring for Gestures"""
    def __init__(self, filepath):
        openni2.initialize()

        device = openni2.Device(filepath)
        # print device.get_sensor_info(openni2.SENSOR_DEPTH)

        self.depth_stream = device.create_depth_stream()

        # depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM, resolutionX = 640, resolutionY = 480, fps = 30))
        self.depth_stream.start()

        print "Frame count: %d" % (self.depth_stream.get_number_of_frames())

    '''
        Source: https://github.com/leezl/OpenNi-Python/blob/master/testPythonOpenni.py
    '''
    def print_frame(frame_data, thisType):
        #need to know what format to get the buffer in:
        # if color pixel type is RGB888, then it must be uint8,
        #otherwise it will split the pixels incorrectly
        img  = np.frombuffer(frame_data, dtype=thisType)
        whatisit = img.size
        #QVGA is what my camera defaulted to, so: 1 x 240 x 320
        #also order was weird (1, 240, 320) not (320, 240, 1)
        if whatisit == (320*240*1):#QVGA
            #shape it accordingly, that is, 1048576=1024*1024
            img.shape = (1, 240, 320)#small chance these may be reversed in certain apis...This order? Really?
            #filling rgb channels with duplicates so matplotlib can draw it (expects rgb)
            img = np.concatenate((img, img, img), axis=0)
            #because the order is so weird, rearrange it (third dimension must be 3 or 4)
            img = np.swapaxes(img, 0, 2)
            img = np.swapaxes(img, 0, 1)
        elif whatisit == (320*240*3):
            #color is miraculously in this order
            img.shape = (240, 320, 3)
        else:
            print "Frames are of size: ",img.size

        #images still appear to be reflected, but I don't need them to be correct in that way
        print img.shape
        #need both of follwoing: plt.imShow adds image to plot
        plt.imshow(img)
        #plt.show shows all the currently added figures
        plt.show()

    def show_frame(self, img):

        # normalize values for display (0..255)
        img = img / 8

        # convert to rgb
        a = np.ndarray(shape=(480,640,3), dtype=np.uint8)
        a[:,:,0] = img
        a[:,:,1] = img
        a[:,:,2] = img

        rgb = cv.fromarray(a)
        # rgb = cv.fromarray(img.squeeze())

        cv.ShowImage('Gestures', rgb)

        # plt.imshow(img.squeeze())
        # plt.show()

    def get_frame(self):
        # do I need this?
        stream = openni2.wait_for_any_stream([self.depth_stream])

        if not stream:
            return None

        # get fresh frame
        frame = stream.read_frame()
        frame_data = frame.get_buffer_as_uint16()

        # prepare frame for rendering
        img = np.frombuffer(frame_data, dtype=np.uint16)
        # img.shape = (1, 480, 640)
        img.shape = (480, 640, 1)

        return img


    def loop(self):

        self.running = True
        while self.running:

            # keep loop running?
            key = cv.WaitKey(5)
            self.running = key in (-1, 32, 112)

            img = self.get_frame()

            # display frame
            self.show_frame(img)

        # tidy up
        self.depth_stream.stop()
        openni2.unload()


class OpenNIKinect(object):

    """docstring for OpenNIKinect"""
    def __init__(self):
        self.handle = Gestures('/Users/flo/projects/master-thesis/S1Hello.oni')

    def get_frame(self, record=False):
        depth = self.handle.get_frame()

        if not len(depth):
            print "NO"

        rgb = np.zeros(shape=(480, 640, 3), dtype=np.uint8)
        channel = depth.copy()
        channel = channel / 32
        rgb[:,:,0] = channel[:,:,0]
        rgb[:,:,1] = channel[:,:,0]
        rgb[:,:,2] = channel[:,:,0]

        # fake rgb
        return (rgb, depth[:,:,0])

    def snapshot():
        pass