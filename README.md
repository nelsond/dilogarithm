# Dilogarithm

This module contains a Python implementation of the
[Dilogarithm](https://en.wikipedia.org/wiki/Spence%27s_function) as a
[numpy ufunc](https://docs.scipy.org/doc/numpy/reference/ufuncs.html)
using a C extension. Note that only real valued arguments are supported
at the moment.

The implementation in the C extension is adapted from the Fortran
implementation in [CERNLIB](http://cernlib.web.cern.ch). See the
[CERNLIB
manual](http://cmd.inp.nsk.su/old/cmd2/manuals/cernlib/shortwrups/node64.html)
for more details. CERNLIB is licensed under the [GNU GPL](http://cernlib.web.cern.ch/cernlib/conditions.html).

## Requirements

This module requires Python >= 3.4.

* `numpy` >= 1.12

## Install

Install with pip

```shell
$ pip install git+git://github.com/nelsond/dilogarithm.git
```

## Example usage

```python
from dilogarithm import rdilog
import numpy as np

rdilog(-100) # => -12.23875517731494

xx = np.linspace(-100, -1, 100)
rdilog(xx) # => array([-12.23875518, -12.19242167, ... ])
```

## Performance

The implementation is fairly fast compared to existing alternatives for
Python (such as the Polylogarithm implementation in mpmath).

```python
In [1]: from random import random
   ...: from dilogarithm import rdilog
   ...: import mpmath as mp

In [2]: %timeit rdilog(random()*1e6)
829 ns ± 41 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

In [3]: %timeit mp.fp.polylog(2, random()*1e6)
14.8 µs ± 196 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
```

The perfomance difference is even more apparent when calculating the
Dilogarithm across a numpy array

```python
In [1]: from random import random
   ...: from dilogarithm import rdilog
   ...: import mpmath as mp
   ...: import numpy as np

In [2]: %timeit rdilog(np.random.rand(10000)*1e6)
711 µs ± 16 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

In [3]: mp_polylog_vec = np.vectorize(mp.fp.polylog,
   ...:                               otypes=(np.complex,), excluded=(0,))

In [3]: %timeit mp_polylog_vec(2, np.random.rand(10000)*1e6)
156 ms ± 1.17 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

(MacBook Pro/2.6 GHz Intel Core i7)
