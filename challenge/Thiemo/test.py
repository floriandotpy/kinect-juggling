import timeit

tests = [
('Summierung uint8',
'''
import pyximport;
import numpy as np
pyximport.install(setup_args={'include_dirs': np.get_include()})
import summierungInt as alg
a = np.random.random_integers(0,255, %(dim)s).astype(np.uint8)
b = np.random.random_integers(0,255, %(dim)s).astype(np.uint8)
''',
'alg.sum(a, b)'),

('Summierung float32',
'''
import pyximport;
import numpy as np
pyximport.install(setup_args={'include_dirs': np.get_include()})
import summierungFloat as alg
a = np.random.random_integers(0,255, %(dim)s).astype(np.float32)
b = np.random.random_integers(0,255, %(dim)s).astype(np.float32)
''',
'alg.sum(a, b)'),

('Schwellenwert uint8',
'''
import pyximport;
import numpy as np
pyximport.install(setup_args={'include_dirs': np.get_include()})
import schwellenwertInt as alg
a = np.random.random_integers(0,255, %(dim)s).astype(np.uint8)
''',
'alg.scalar(a, 125)'),

('Schwellenwert float32',
'''
import pyximport;
import numpy as np
pyximport.install(setup_args={'include_dirs': np.get_include()})
import schwellenwertFloat as alg
a = np.random.random_integers(0,255, %(dim)s).astype(np.float32)
''',
'alg.scalar(a, 125.0)'),

('Histogramm uint8',
'''
import pyximport;
import numpy as np
pyximport.install(setup_args={'include_dirs': np.get_include()})
import histogrammInt as alg
a = np.random.random_integers(0,255, %(dim)s).astype(np.uint8)
''',
'alg.histogramm(a)'),

('Histogramm float32',
'''
import pyximport;
import numpy as np
pyximport.install(setup_args={'include_dirs': np.get_include()})
import histogrammFloat as alg
a = np.random.random_integers(0,255, %(dim)s).astype(np.float32)
''',
'alg.histogramm(a)')
]

for name, setup, cmd in tests:
    for dim in ('(204,204)','(409,409)'):
        print '%s %s: %f' % (name, dim, timeit.timeit(cmd, setup=setup % {'dim' : dim}, number=100))
