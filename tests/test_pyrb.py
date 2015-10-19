#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pyrubberband
import numpy as np

from nose.tools import raises

def test_stretch():

    sr = 8000
    duration = 5
    y = np.zeros(sr * duration)

    def __test(rate):
        y_s = pyrubberband.time_stretch(y, sr, rate=rate)

        assert np.allclose(rate * len(y_s), len(y))

    for rate in [0.5, 1.0, 2.0]:
        yield __test, rate

    for bad_rate in [-1, -0.5, 0]:
        yield raises(ValueError)(__test), bad_rate
