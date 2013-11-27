from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy as np

setup (
    name = 'Sum arrays',
    cmdclass = { 'build_ext': build_ext },
    ext_modules = [
        Extension ( "cy_sum_arrays",
        ["cy_sum_arrays.pyx"],
        include_dirs =[ np.get_include()]),
    ])