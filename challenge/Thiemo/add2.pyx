import numpy as np

def my_add(a, b):
    if a.shape != b.shape:
        raise ValueError("Arrays must have identical dimensions")
    if a.dtype != b.dtype:
        raise ValueError("Arrays must have identical type")

    dtype = a.dtype
    height = a.shape[0]
    width = a.shape[1]

    result = np.zeros((height, width), dtype=dtype)

    for y in range(height):
        for x in range(width):
            result[y,x] = a[y,x] + b[y,x]

    return result

