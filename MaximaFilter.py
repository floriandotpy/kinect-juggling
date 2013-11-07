import numpy as np
import cv
import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters

class MaximaFilter(object):

    def filter(self, rgb, depth, argv = {}):
        # TODO ROLF
        # http://stackoverflow.com/questions/9111711/get-coordinates-of-local-maxima-in-2d-array-above-certain-value
        neighborhood_size = 50
        threshold = 1500


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

        # return cv.fromarray(np.array(rgb[:,:,::-1], dtype=np.uint8)), depth

        return rgb, depth

        # return maxima