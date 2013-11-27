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
#
# "cimport" is used to import special compile-time information
# about the numpy module (this is stored in a file numpy.pxd which is
# currently part of the Cython distribution).
cimport numpy as np
# We now need to fix a datatype for our arrays. I've used the variable
# DTYPE for this, which is assigned to the usual NumPy runtime
# type info object.
DTYPE = np.uint8
# "ctypedef" assigns a corresponding compile-time type to DTYPE_t. For
# every type in the numpy module there's a corresponding compile-time
# type with a _t-suffix.
ctypedef np.int_t DTYPE_t
# "def" can type its arguments but not have a return type. The type of the
# arguments for a "def" function is checked at run-time when entering the
# function.
#
# The arrays f, g and h is typed as "np.ndarray" instances. The only effect
# this has is to a) insert checks that the function arguments really are
# NumPy arrays, and b) make some attribute access like f.shape[0] much
# more efficient. (In this example this doesn't matter though.)
def cy_sum_arrays_int(np.ndarray a, np.ndarray b):
    if a.shape[0] != b.shape[0] or a.shape[1] != b.shape[1]:
        raise ValueError("Arrays must have identical dimenstions")
    assert a.dtype == DTYPE and b.dtype == DTYPE
    # The "cdef" keyword is also used within functions to type variables. It
    # can only be used at the top indendation level (there are non-trivial
    # problems with allowing them in other places, though we'd love to see
    # good and thought out proposals for it).
    #
    # For the indices, the "int" type is used. This corresponds to a C int,
    # other C types (like "unsigned int") could have been used instead.
    # Purists could use "Py_ssize_t" which is the proper Python type for
    # array indices.
    cdef int width = a.shape[0]
    cdef int height = a.shape[1]
    cdef np.ndarray out = np.zeros([width, height], dtype=DTYPE)
    cdef int x, y, s, t, v, w
    # It is very important to type ALL your variables. You do not get any
    # warnings if not, only much slower code (they are implicitly typed as
    # Python objects).
    cdef int s_from, s_to, t_from, t_to
    # For the value variable, we want to use the same data type as is
    # stored in the array, so we use "DTYPE_t" as defined above.
    # NB! An important side-effect of this is that if "value" overflows its
    # datatype size, it will simply wrap around like in C, rather than raise
    # an error like in Python.
    cdef DTYPE_t value
    for x in range(width):
        for y in range(height):
            value = a[x, y] + b[x, y]
            out[x, y] = value
    return out