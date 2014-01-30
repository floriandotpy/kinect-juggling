import cv
import numpy as np
from KinectDummy import KinectDummy

# b = 80 # Winkel, in dem hochgeworfen wird
# v = 100 # Geschwindigkeit des Balles
# t = 1 # Zeitpunkt
# g = 9.81

def trajectory((x1, y1), (x2, y2), t):
	b = np.degrees(np.arctan((y1-y2)/(x2-x1)))
	# b = np.arctan((y2-y1)/(x2-x1))
	v = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
	x = (v * t * np.cos(b)) + x2
	y = 490 - ((v * t * np.sin(b) - (9.81/2) * t**2) + y2)
	return (int(x),int(y))

kinect = KinectDummy()
for i in xrange(30):
	(rgb, depth) = kinect.get_frame()

# (x, y)
p1 = (250, 285)
p2 = (255, 245)
points = []

for t in xrange(10):
	(x,y) = trajectory(p1, p2, t)
	points.append((x,y))
	# print (x,y)
	cv.Circle(cv.fromarray(rgb), (x,y), int(abs(3)), cv.RGB(0, 0, 255), thickness=-1, lineType=8, shift=0)

# print points

#for (x,y,r) in circles:
#cv.Circle(cv.fromarray(rgb), (int(x),int(y)), int(abs(r)), cv.RGB(0, 0, 255), thickness=-1, lineType=8, shift=0)
cv.Circle(cv.fromarray(rgb), (p1), int(abs(1)), cv.RGB(0, 255, 0), thickness=-1, lineType=8, shift=0)
cv.Circle(cv.fromarray(rgb), (p2), int(abs(1)), cv.RGB(0, 255, 0), thickness=-1, lineType=8, shift=0)

img = cv.fromarray(np.array(rgb[:,:,::-1]))
cv.ShowImage('display', img)
cv.WaitKey(0)