import numpy as np
from scipy import ndimage

import timeit as ti


test_configs = ("Testcase 1: small shape, pixeltype: uint8",
                "Testcase 2: large shape, pixeltype: uint8",
                "Testcase 3: small shape, pixeltype: float",
                "Testcase 4: large shape, pixeltype: float")


setup_string = """
import numpy as np
from scipy import ndimage
#import pyximport; pyximport.install()
import cy_sum_arrays
import sum_arrays

small_shape = (2048, 2048)
large_shape = (4096, 4096)

test_images = ((np.random.random_integers(0,255, small_shape).astype(np.uint8), np.random.random_integers(0,255, small_shape).astype(np.uint8)),
               (np.random.random_integers(0,255, large_shape).astype(np.uint8), np.random.random_integers(0,255, large_shape).astype(np.uint8)))

thresh = 128

mask = np.array([[1, 4, 7, 4, 1],
                 [4,16,26,16, 4],
                 [7,26,41,26, 7],
                 [4,16,26,16, 4],
                 [1, 4, 7, 4, 1]])/273.0

theta = 33.7
                 """
number_of_executions = 100


tests = (("1",  "Summation of arrays, actual cython",    "img_dest = cy_sum_arrays.cy_sum_arrays_int(test_images[{i}][0], test_images[{i}][0])"),
        ("2", "Summation of arrays, numby", "img_dest = test_images[{i}][0] + test_images[{i}][1]" ),
        #("1", "Summation of arrays, vanilla python",   "img_dest = sum_arrays.py_sum_arrays(test_images[{i}][0], test_images[{i}][0])"),
        ("3",  "Summation of arrays, python in cython", "img_dest = cy_sum_arrays.py_sum_arrays(test_images[{i}][0], test_images[{i}][0])"))
         # ("2",  "Thresholding of images",                                        "img_dest = test_images[{i}][0] > thresh"),
         # ("3",  "Histogram of images",                                           "img_hist = np.histogram(test_images[{i}][0], bins=256, range=(0,255))"),
         # ("4a", "2d-convolution of images with gaussian mask (size: 5x5)",       "img_dest = ndimage.convolve(test_images[{i}][0],mask)"),
         # ("4b", "2d-sep-conv. of images with two 1d-gaussians (sizes: 5x1,1x5)", "img_dest = ndimage.gaussian_filter(test_images[{i}][0],1.0)"),
         # ("5",  "Anisotropic median filter (size: 5x5)",                         "img_dest = ndimage.median_filter(test_images[{i}][0],5)"),
         # ("6",  "Subsampling of images",                                         "img_dest = (test_images[{i}][0][::2,::2]+test_images[{i}][0][1::2,0::2]+test_images[{i}][0][0::2,1::2]+test_images[{i}][0][1::2,1::2])/4.0"),
         # ("7", "Rotation of images (with linear interpolation)",                 "img_dest = ndimage.rotate(test_images[{i}][0],theta, order=1)"))


for test in tests:
    print "Running test ", test[0], ": ", test[1], ":"
    for i in range(2):
        print "   ", test_configs[i], "time :", \
        ti.timeit(test[2].format(i=i), setup=setup_string, number=number_of_executions)