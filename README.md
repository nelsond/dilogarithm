# Dilogarithm [![Build Status](https://travis-ci.org/nelsond/dilogarithm.svg?branch=master)](https://travis-ci.org/nelsond/dilogarithm)

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

**Note:** [`scipy.special.spence`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.spence.html) is equivalent to the `rdilog` implementation in this module when changing the argument accordingly.

```python
from scipy.special import spence

def rdilog(x):
	return spence(1-x)
```

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

The performance of this module is comparable to `scipy.special.spence` and faster than `mpmath.fp.polylogy`.

```python
In [1]: from random import random
   ...: from dilogarithm import rdilog
   ...: from scipy.special import spence
   ...: import mpmath as mp

In [2]: %timeit rdilog(random()*1e6)
779 ns ± 22.3 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

In [3]: %timeit spence(random()*1e6)
794 ns ± 19.1 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

In [4]: %timeit mp.fp.polylog(2, random()*1e6)
14.7 µs ± 757 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
```

(MacBook Pro/2.6 GHz Intel Core i7)
