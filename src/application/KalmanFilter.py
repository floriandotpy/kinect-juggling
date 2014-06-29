import cv
import numpy as np

# b = 80 # Winkel, in dem hochgeworfen wird
# v = 100 # Geschwindigkeit des Balles
# t = 1 # Zeitpunkt
# g = 9.81

class KalmanFilter(object):

	def __init__(self):
		self.point0 = (0,0)
		self.point1 = (1,1)

	def trajectory(self, (y1, x1), (y2, x2), t):
		b = np.degrees(np.arctan((y2-y1)/(x2-x1)))
		# b = np.arctan((y2-y1)/(x2-x1))
		v = np.sqrt((x1 + x2)**2 + (y1 + y2)**2)
		x = v * t * np.degrees(np.cos(b))
		y = v * t * np.degrees(np.sin(b) - (9.81/2) * t**2)
		return (y,x)

	def filter(self, rgb, depth, balls, args = {}):
		p1 = (480, 0)
		p2 = (470, 10)
		points = []

		for t in xrange(1,3):
			point = self.trajectory(p1, p2, t)
			points.append(point)
			print point

   #      for (x,y) in points:
			# cv.Circle(cv.fromarray(rgb), (int(x),int(y)), int(abs(r)), cv.RGB(0, 0, 255), thickness=-1, lineType=8, shift=0)

		return rgb, depth, balls