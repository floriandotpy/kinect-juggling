class DelayedBuffer(object):
    """Reduces noise on the depth image. """
    def __init__(self, buffersize=3):
        self.buffersize = buffersize
        self.buffers = [None for _ in xrange(buffersize)]
        self.buffer_i = 0

    def add(self, depth):
        """ Add a depth image to the buffer """
        self.buffers[self.buffer_i] = depth
        self.buffer_i = (self.buffer_i + 1) % self.buffersize

    def get(self):
        """ Returns an older depth image """
        return self.buffers[self.buffer_i]