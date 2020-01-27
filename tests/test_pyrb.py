#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import numpy as np
import pytest

from contextlib2 import nullcontext as dnr

import pyrubberband


def synth(sr, num_samples, freq):
    return np.sin(
        2 * np.pi * (freq / sr) * np.linspace(
            0, 1, num=num_samples
        )
    )


@pytest.fixture(params=([1, 2]))
def length(request):
    return request.param


@pytest.fixture(params=([16000, 44100, 48000]))
def sr(request):
    return request.param


@pytest.fixture
def num_samples(length, sr, request):
    return int(length * sr)


@pytest.fixture(params=([500.0, 440.0, 123.0]))
def freq(request):
    return request.param


@pytest.fixture(params=([-1.5, -1, -0.5, 0, 0.5, 1, 1.5]))
def n_step(request):
    return request.param


@pytest.fixture(params=([None, 1, 2, 6]))
def channels(request):
    return request.param


@pytest.fixture
def time_map(num_samples, request):
    return [(0, 0),
            (num_samples//4, num_samples//4),
            ((3*num_samples)//4, num_samples//2),
            (num_samples, (3*num_samples)//4)]


@pytest.fixture
def random_signal(channels, num_samples):
    if channels is not None:
        shape = (num_samples, channels)
    else:
        shape = (num_samples,)
    return np.random.random(shape)


@pytest.mark.parametrize(
    "rate,ctx",
    [
        (0.5, dnr()),
        (1.0, dnr()),
        (2.0, dnr()),
        (-1, pytest.raises(ValueError)),
        (-0.5, pytest.raises(ValueError)),
        (0, pytest.raises(ValueError)),
    ]
)
def test_stretch(sr, random_signal, num_samples, rate, ctx):
    '''Test shape of random signals with stretching
    factor of various rate.
    '''

    # input signal of shape (channels, sr * duration)
    y = random_signal

    with ctx:
        y_s = pyrubberband.time_stretch(y, sr, rate=rate)

        # test if output dimension matches input dimension
        assert y_s.ndim == y.ndim

        # check shape
        if y.ndim > 1:
            # check number of channels
            assert y.shape[1] == y_s.shape[1]
        else:
            # check num_samples (stretching factor)
            assert np.allclose(y_s.shape[0] * rate, y.shape[0])


def test_pitch(sr, num_samples, freq, n_step):

    y = synth(sr, num_samples, freq)

    y_s = pyrubberband.pitch_shift(y, sr, n_step)

    # Make sure we have the same duration
    assert np.allclose(len(y), len(y_s))

    # compare to directly synthesize target track

    # we'll compare normalized power spectra to avoid phase issues
    t_freq = freq * 2.0**(n_step / 12.0)
    y_f = synth(sr, num_samples, t_freq)

    s_s = np.abs(np.fft.rfft(y_s))
    s_f = np.abs(np.fft.rfft(y_f))

    assert np.allclose(s_s / s_s[0], s_f / s_f[0], atol=1e-2)


@pytest.mark.parametrize(
    "time_map,ctx",
    [
        ([(0, 0), (16000, -8000)], pytest.raises(ValueError)),
        ([(0, 0), (-16000, 8000)], pytest.raises(ValueError)),
        ([(0, 0), (12000, 8000)], pytest.raises(ValueError)),
        ([(0, 0), (8000, 6000), (4000, 4000), (16000, 12000)],
         pytest.raises(ValueError))
    ]
)
def test_fails_timemap_stretch(time_map, ctx):
    sr, num_samples, freq = 16000, 16000, 500
    y = np.cos(2 * np.pi * freq * np.arange(num_samples)/sr)

    with ctx:
        # Apply time strech
        y_s = pyrubberband.timemap_stretch(y, sr, time_map)

        assert np.isclose(len(y_s), time_map[-1][1], rtol=1e-3)

        # Make sure that the peak frequency of `y_s` is `freq`
        n = len(y_s)
        fft = np.abs(np.fft.fft(y_s))
        peak_freq = np.argmax(fft[:n//2]) * sr / n

        assert np.isclose(peak_freq, freq, rtol=1e-1)


def test_timemap_stretch(sr, num_samples, freq, time_map):

    y = np.cos(2 * np.pi * freq * np.arange(num_samples)/sr)
    # Apply time strech
    y_s = pyrubberband.timemap_stretch(y, sr, time_map)

    assert np.isclose(len(y_s), time_map[-1][1], rtol=1e-3)

    # Make sure that the peak frequency of `y_s` is `freq`
    n = len(y_s)
    fft = np.abs(np.fft.fft(y_s))
    peak_freq = np.argmax(fft[:n//2]) * sr / n

    assert np.isclose(peak_freq, freq, rtol=1e-1)


@pytest.mark.parametrize(
    "cli,ctx",
    [('rubberband-missing', pytest.raises(RuntimeError)),
     ('rubberband', dnr())])
def test_missing_cli(cli, ctx):
    '''Simulate not having rubberband-cli installed and check for
    the appropriate exception.
    '''

    with ctx:
        pyrubberband.pyrb.__RUBBERBAND_UTIL = cli
        pyrubberband.pitch_shift(np.random.randn(22050), 22050, 1)
