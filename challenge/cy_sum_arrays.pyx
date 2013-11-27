def py_sum_arrays(a, b):
    width = len(a[0])
    height = len(a)
    c = [[0 for _inner in xrange(width)] for _outer in xrange(height)]
    for y in xrange(height):
        for x in xrange(width):
            c[y][x] = a[y][x] + b[y][x]
    return c

# def cy_sum_arrays_int(int[:,:] a, int[:,:] b):
#     cdef int width, height
#     cdef int[:,:] c
#     width = len(a[0])
#     height = len(a)
#     c = [[0 for _inner in xrange(width)] for _outer in xrange(height)]
#     for y in xrange(height):
#         for x in xrange(width):
#             c[y][x] = a[y][x] + b[y][x]
#     return c


import numpy as np
cimport numpy as np
DTYPE = np.uint8
ctypedef np.uint8_t DTYPE_t
cimport cython

@cython.boundscheck(False)
def cy_sum_arrays_int(np.ndarray[DTYPE_t, ndim=2] a, np.ndarray[DTYPE_t, ndim=2] b):
    cdef int width = a.shape[0]
    cdef int height = a.shape[1]
    cdef np.ndarray out = np.zeros([width, height], dtype=DTYPE)

    cdef int x, y, s, t, v, w
    cdef DTYPE_t value

    for x in range(width):
        for y in range(height):
            value = a[x, y] + b[x, y]
            out[x, y] = value
    return out