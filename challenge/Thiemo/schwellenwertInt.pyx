import numpy as np
cimport numpy as np
cimport cython

DTYPE = np.uint8
ctypedef np.uint8_t DTYPE_t

@cython.boundscheck(False)
def scalar(np.ndarray[DTYPE_t, ndim=2] a, int scalar):
    if a.dtype != DTYPE:
        raise ValueError("Arrays must have type %s" % DTYPE)

    cdef int height = a.shape[0]
    cdef int width = a.shape[1]

    cdef np.ndarray[DTYPE_t, ndim=2] result = np.zeros((height, width), dtype=DTYPE)

    cdef int x, y

    for x in range(width):
        for y in range(height):
            result[y,x] = a[y,x] if a[y,x] > scalar else 0

    return result