def py_sum_arrays(a, b):
    width = len(a[0])
    height = len(a)
    c = [[0 for _inner in xrange(width)] for _outer in xrange(height)]
    for y in xrange(height):
        for x in xrange(width):
            c[y][x] = a[y][x] + b[y][x]
    return c
