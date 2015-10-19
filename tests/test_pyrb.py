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


def synth(sr, duration, freq):

    return np.sin(2 * np.pi * (freq / sr) * np.linspace(0, 1, num=duration * sr))

def test_pitch():

    sr = 8000
    duration = 5
    freq = 500.0
    y = synth(sr, duration, freq)

    def __test(n_steps):

        y_s = pyrubberband.pitch_shift(y, sr, n_steps)

        # Make sure we have the same duration
        assert np.allclose(len(y), len(y_s))

        # compare to directly synthesize target track

        # we'll compare normalized power spectra to avoid phase issues
        t_freq = freq * 2.0**(n_steps / 12.0)
        y_f = synth(sr, duration, t_freq)

        s_s = np.abs(np.fft.rfft(y_s))
        s_f = np.abs(np.fft.rfft(y_f))

        assert np.allclose(s_s / s_s[0], s_f / s_f[0], atol=1e-2)

        
    for n_steps in [-1.5, -1, -0.5, 0, 0.5, 1, 1.5]:

        yield __test, n_steps
