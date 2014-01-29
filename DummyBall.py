import math

class DummyBall(object):

    """A DummyBall is an artificial object that tries to behave in gravity the same
    way a real ball would do."""

    def __init__(self, position=(0,0)):

        self.time = 0
        self.radius = 15

        self.x_speed = 1 #-0.05
        self.x_offset = 270
        self.x_stretch = 200

        self.y_speed = 0.07
        self.y_offset = 100
        self.y_stretch = 220.0

    @property
    def position(self):
        self.time += 1
        x = self.x(self.time)
        y = self.y(self.time)
        print "x: %d" % x
        print "y: %d" % y
        return (x, y)


    def x(self, time):
        # return 0
        return int(self.x_offset + ((time * (1 if time % self.x_stretch*2 < self.x_stretch else -1))) % self.x_stretch*2)
        # a float value between 0.0 and 1.0
        clock = (math.sin(time*self.x_speed)+1)/2
        return int(self.x_offset + clock*self.x_stretch)

    def y(self, time):

        # a float value between 0.0 and 1.0
        clock = ((time * 1.0) % self.y_stretch)/self.y_stretch
        print clock
        return self.y_offset + int(clock**2.0 * self.y_stretch)
        return int(self.y_offset + (((time * (1 if time % self.y_stretch*2 < self.y_stretch else -1)))**2/self.y_stretch) % self.y_stretch*2)
        return self.y_offset + int((((time % self.y_stretch)/self.y_stretch) ** 2)*self.y_stretch)
        # a float value between 0.0 and 1.0
        clock = (math.cos(time*self.y_speed)+1)/2
        return int(self.y_offset + clock*self.y_stretch)




