import timeit

# import pyximport; pyximport.install()
# import doit
# import cy_sum_arrays as flo
# import numpy as np

setup = '''
import pyximport;
import numpy as np
pyximport.install(setup_args={'include_dirs': np.get_include()})
import doit
a = np.random.random_integers(0,255, (10,10)).astype(np.uint8)
'''

print 'time: %f' % timeit.timeit('doit.my_function(a, a)', setup=setup, number=10000)

# flo.py_sum_arrays(a,a)