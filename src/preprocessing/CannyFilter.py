import numpy as np
import cv, cv2
try:
    import vigra as vi
except Exception, e:
    pass

class CannyFilter(object):

    # def filter(self, rgb, depth, argv = {}):

    #     img = cv.fromarray(depth, cv.CV_8UC1)
    #     mat1 = cv.CreateMat(img.rows, img.cols, cv.CV_8UC1)
    #     mat2 = cv.CreateMat(img.rows, img.cols, cv.CV_8UC1)
    #     cv.Convert(img, mat1)
    #     cv.Canny(mat1, mat2, 50, 200) # ???

    #     return rgb, np.asarray(mat2)

    def filter(self, rgb, depth, balls, argv = {}):

		img = np.asarray(depth)
		# img = cv.fromarray(depth, cv.CV_8UC1)
		# mat = cv.CreateMat(img.rows, img.cols, cv.CV_8UC1)
		# cv.Convert(img, mat)
		img = cv2.GaussianBlur(img,(3,3),0)
		# img = cv2.Canny(img,10,100,apertureSize=3)
		# cv.Canny(img,edges,0,300,aperture_size=3)

		im = vi.Image(img, dtype=np.uint8)
		edgels = vi.analysis.cannyEdgelList(im,3.0,3.0)

		# img = cv2.Canny(img, 50, 200)
		# rgb = cv2.cvtColor(img, cv.CV_GRAY2BGR)
		print edgels

		w, h = img.shape
		rgb = np.empty((w, h, 3), dtype=np.uint8)
		rgb[:, :, :] = img[:, :, np.newaxis]

		return rgb, depth, balls