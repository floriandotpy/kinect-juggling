import timeit

setup = '''
import numpy as np
import add1 as add

a = np.random.random_integers(0,255, (128,128)).astype(np.uint8)
b = np.random.random_integers(0,255, (128,128)).astype(np.uint8)
'''
print 'time python (128,128): %f' % timeit.timeit('add.my_add(a, b)', setup=setup, number=100)

setup = '''
import numpy as np
import pyximport; pyximport.install()
import add2 as add

a = np.random.random_integers(0,255, (128,128)).astype(np.uint8)
b = np.random.random_integers(0,255, (128,128)).astype(np.uint8)
'''
print 'time python as cython: %f' % timeit.timeit('add.my_add(a, b)', setup=setup, number=100)

setup = '''
import numpy as np
import pyximport; pyximport.install(setup_args={'include_dirs': np.get_include()})
import add3 as add

a = np.random.random_integers(0,255, (128,128)).astype(np.uint8)
b = np.random.random_integers(0,255, (128,128)).astype(np.uint8)
'''
print 'time cython typed: %f' % timeit.timeit('add.my_add(a, b)', setup=setup, number=100)

setup = '''
import numpy as np
import pyximport; pyximport.install(setup_args={'include_dirs': np.get_include()})
import add4 as add

a = np.random.random_integers(0,255, (2048,2048)).astype(np.uint8)
b = np.random.random_integers(0,255, (2048,2048)).astype(np.uint8)
'''
print 'time cython array access: %f' % timeit.timeit('add.my_add(a, b)', setup=setup, number=100)

setup = '''
import numpy as np
import pyximport; pyximport.install(setup_args={'include_dirs': np.get_include()})
import add5 as add

a = np.random.random_integers(0,255, (2048,2048)).astype(np.uint8)
b = np.random.random_integers(0,255, (2048,2048)).astype(np.uint8)
'''
print 'time cython without boundscheck: %f' % timeit.timeit('add.my_add(a, b)', setup=setup, number=100)

setup = '''
import numpy as np

a = np.random.random_integers(0,255, (2048,2048)).astype(np.uint8)
b = np.random.random_integers(0,255, (2048,2048)).astype(np.uint8)
'''
print 'time numpy: %f' % timeit.timeit('a + b', setup=setup, number=100)

setup = '''
import numpy as np
import pyximport; pyximport.install(setup_args={'include_dirs': np.get_include()})
import add6 as add

a = np.random.random_integers(0,255, (2048,2048)).astype(np.uint8)
b = np.random.random_integers(0,255, (2048,2048)).astype(np.uint8)
'''
print 'time numpy in cython: %f' % timeit.timeit('add.my_add(a, b)', setup=setup, number=100)