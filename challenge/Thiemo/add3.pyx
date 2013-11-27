import numpy as np
cimport numpy as np

DTYPE = np.uint8
ctypedef np.uint8_t DTYPE_t

def my_add(np.ndarray a, np.ndarray b):
    if a.shape[0] != b.shape[0] or a.shape[1] != b.shape[1]:
        raise ValueError("Arrays must have identical dimensions")
    if a.dtype != DTYPE or b.dtype != DTYPE:
        raise ValueError("Arrays must have type %s" % DTYPE)

    cdef int height = a.shape[0]
    cdef int width = a.shape[1]

    cdef np.ndarray result = np.zeros((height, width), dtype=DTYPE)

    cdef int x, y

    for y in range(height):
        for x in range(width):
            result[y,x] = a[y,x] + b[y,x]

    return result

