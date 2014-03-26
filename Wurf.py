import cv
import numpy as np
from KinectDummy import KinectDummy


def trajectory((x1, y1), (x2, y2), t):

    # gravity, positive because y is upside-down
    g   = 9.81

    # speed in x and y direction
    v_x = x2 - x1
    v_y = y2 - y1

    # beta, arc of throw direction
    b   = np.arctan(v_y / v_x)

    # distance in x and y direction
    x   = v_x * t + x2
    y   = v_y * t + g/2 * t**2 + y2

    return int(x), int(y)


kinect = KinectDummy()
for i in xrange(30):
    (rgb, depth) = kinect.get_frame()

def draw(p1, p2):

    # print points
    p1 = (int(p1[0]), int(p1[1]))
    p2 = (int(p2[0]), int(p2[1]))

    for t in xrange(15):
        (x,y) = trajectory(p1, p2, t)

        print "t = %d \t(x,y) = %d, %d" % (t, x,y)

        cv.Circle(cv.fromarray(rgb), (x,y), int(abs(3)), cv.RGB(0, 255 if t is 0 else 0, 255), thickness=-1, lineType=8, shift=0)


p1 = (290.0, 350.0)
p2 = (300.0, 290.0)
draw(p1, p2)


# show
img = cv.fromarray(np.array(rgb[:,:,::-1]))
cv.ShowImage('display', img)
cv.WaitKey(0)
