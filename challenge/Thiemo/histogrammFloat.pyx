import numpy as np
cimport numpy as np
cimport cython

DTYPE = np.float32
ctypedef np.float32_t DTYPE_t

@cython.boundscheck(False)
def histogramm(np.ndarray[DTYPE_t, ndim=2] a):
    if a.dtype != DTYPE:
        raise ValueError("Arrays must have type %s" % DTYPE)

    cdef int height = a.shape[0]
    cdef int width = a.shape[1]

    cdef np.ndarray[np.uint8_t, ndim=1] result = np.zeros(256, dtype=np.uint8)

    cdef int x, y

    cdef np.ndarray[np.uint8_t, ndim=2] aint = a.astype(np.uint8)

    for x in range(width):
        for y in range(height):
            result[aint[y,x]] += 1

    return result