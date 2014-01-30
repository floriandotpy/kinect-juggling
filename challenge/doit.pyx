# from __future__ import division
import numpy as np
cimport numpy as np
cimport cython

# cdef inline int int_max(int a, int b): return a if a >= b else b
# cdef inline int int_min(int a, int b): return a if a <= b else b

@cython.boundscheck(False) # turn of bounds-checking for entire function
def my_function(np.ndarray[np.uint8_t, ndim=2] a, np.ndarray[np.uint8_t, ndim=2] b):
    if a.shape != b.shape:
        raise ValueError('Arrays must have identical dimensions')
    if a.dtype is not np.uint8 or b.dtype is not np.uint8:
        raise ValueError('Array type %s not supported' % a.dtype)

    cdef np.ndarray[np.uint8_t, ndim=2] n = np.zeros([a.shape[0], a.shape[1]], dtype=np.uint8)

    cdef int x, y

    for x in range(a.shape[0]):
        for y in range(a.shape[1]):
            n[x,y] = a[x,y] + b[x,y]

    return a, b, n
