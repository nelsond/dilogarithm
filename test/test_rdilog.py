import pytest

import numpy as np
from numpy import pi, log, sqrt

from dilogarithm import rdilog

EPS = 1e-14


# See https://en.wikipedia.org/wiki/Spence%27s_function#Special%20values
def test_rdilog_special_values():
    assert rdilog(-1) == pytest.approx(-pi**2/12, EPS)

    assert rdilog(0) == pytest.approx(0, EPS)

    assert rdilog(1/2) == pytest.approx(pi**2/12 - log(2)**2/2, EPS)

    assert rdilog(1) == pytest.approx(pi**2/6, EPS)

    assert rdilog(2) == pytest.approx((pi**2/4 - 1j*pi*log(2)).real, EPS)

    assert rdilog(-(sqrt(5) - 1) / 2) == \
        pytest.approx(-pi**2/15 + 0.5*log((sqrt(5) + 1) / 2)**2, EPS)

    assert rdilog(-(sqrt(5) + 1) / 2) == \
        pytest.approx(-pi**2/10 - log((sqrt(5) + 1) / 2)**2, EPS)

    assert rdilog((3 - sqrt(5)) / 2) == \
        pytest.approx(pi**2/15 - log((sqrt(5) + 1) / 2)**2, EPS)

    assert rdilog((sqrt(5) - 1) / 2) == \
        pytest.approx(pi**2/10 - log((sqrt(5) + 1) / 2)**2, EPS)


# See https://en.wikipedia.org/wiki/Spence%27s_function#Identities
def test_rdilog_identies():
    xx = np.logspace(-5, 5, 10000)

    assert (rdilog(xx) + rdilog(-xx)) == \
        pytest.approx(0.5 * rdilog(xx**2), EPS)

    assert (rdilog(1 - xx) + rdilog(1 - 1/xx)) == \
        pytest.approx(-log(xx)**2/2, EPS)

    assert (rdilog(xx) + rdilog(1 - xx)) == \
        pytest.approx(pi**2/6 - log(xx) * log((1 + 0j) - xx).real, EPS)

    assert (rdilog(-xx) - rdilog(1 - xx) + 0.5*rdilog(1-xx**2)) == \
        pytest.approx(-pi**2/12 - log(xx) * log(xx + 1), EPS)

    assert (rdilog(-xx) - rdilog(1 - xx) + 0.5*rdilog(1-xx**2)) == \
        pytest.approx(-pi**2/12 - log(xx) * log(xx + 1), EPS)

    assert (rdilog(xx) + rdilog(1 / xx)) == \
        pytest.approx(-pi**2/6 - 0.5*(log(0j-xx)**2).real, EPS)


# See
# https://en.wikipedia.org/wiki/Spence%27s_function#Particular%20value%20identities
def test_rdilog_value_identies():
    assert (rdilog(1/3) - 1/6 * rdilog(1/9)) == \
        pytest.approx(pi**2/18 - log(3)**2/6, EPS)

    assert (rdilog(-1/2) + 1/6 * rdilog(1/9)) == \
        pytest.approx(-pi**2/18 + log(2) * log(3) - log(2)**2/2 - log(3)**2/3,
                      EPS)

    assert (rdilog(1/4) + 1/3 * rdilog(1/9)) == \
        pytest.approx(pi**2/18 + 2 * log(2) * log(3) - 2 * log(2)**2 -
                      2/3 * log(3)**2, EPS)

    assert (rdilog(-1/3) - 1/3 * rdilog(1/9)) == \
        pytest.approx(-pi**2/18 + 1/6 * log(3)**2, EPS)

    assert (rdilog(-1/8) + rdilog(1/9)) == \
        pytest.approx(-1/2*log(9/8)**2, EPS)

    assert (36*rdilog(1/2) - 36*rdilog(1/4) -
            12*rdilog(1/8) + 6*rdilog(1/64)) == pytest.approx(pi**2, EPS)
