class Filter(object):

    # def __init__(self, *args, **kwargs):
        # self.attributes = [attr for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith('__')]

    def process(self, args):
        for attr, attr_type in self.required.iteritems():
            if attr not in args:
                raise Exception('Filter argument %s is missing.' % attr)
            if not isinstance(args[attr], attr_type):
                raise Exception('Filter argument %s must be %s.' % (attr, attr_type))
            setattr(self, attr, args[attr])
        self.filter()

    def filter(self):
        pass


from src.balldetection.SimpleHandBall import SimpleHandBallCollection

class FilterSubclass(Filter):

    required = {
        'centerX': int,
        'balls': SimpleHandBallCollection,
    }

    def filter(self):
        print self.centerX
        print self.balls

filter = FilterSubclass()
filter.process({
    'centerX': 12,
    'balls': SimpleHandBallCollection(),
})
