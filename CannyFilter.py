import numpy as np
import cv

class CannyFilter(object):

    def filter(self, rgb, depth, argv = {}):

        img = cv.fromarray(depth, cv.CV_8UC1)
        mat1 = cv.CreateMat(img.rows, img.cols, cv.CV_8UC1)
        mat2 = cv.CreateMat(img.rows, img.cols, cv.CV_8UC1)
        cv.Convert(img, mat1)
        cv.Canny(mat1, mat2, 50, 200) # ???

        return rgb, np.asarray(mat2)