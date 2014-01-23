import numpy as np
cimport numpy as np
cimport cython

DTYPE = np.float32
ctypedef np.float32_t DTYPE_t

@cython.boundscheck(False)
def sum(np.ndarray[DTYPE_t, ndim=2] a, np.ndarray[DTYPE_t, ndim=2] b):
    if a.shape[0] != b.shape[0] or a.shape[1] != b.shape[1]:
        raise ValueError("Arrays must have identical dimensions")
    if a.dtype != DTYPE or b.dtype != DTYPE:
        raise ValueError("Arrays must have type %s" % DTYPE)

    cdef int height = a.shape[0]
    cdef int width = a.shape[1]

    cdef np.ndarray[DTYPE_t, ndim=2] result = np.zeros((height, width), dtype=DTYPE)

    cdef int x, y

    for x in range(width):
        for y in range(height):
            result[y,x] = a[y,x] + b[y,x]

    return result

