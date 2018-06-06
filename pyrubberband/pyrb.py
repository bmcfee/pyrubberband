#!/usr/bin/env python
# CREATED:2015-03-02 11:36:15 by Brian McFee <brian.mcfee@nyu.edu>
'''Command-line wrapper for rubberband

.. autosummary::
    :toctree: generated/

    time_stretch
    pitch_shift
'''


import os
import six
import subprocess
import tempfile
import numpy as np
import soundfile as sf


__all__ = ['time_stretch', 'pitch_shift', 'timemap_stretch']

__RUBBERBAND_UTIL = 'rubberband'

if six.PY2:
    DEVNULL = open(os.devnull, 'w')
else:
    DEVNULL = subprocess.DEVNULL


def __rubberband(y, sr, **kwargs):
    '''Execute rubberband

    Parameters
    ----------
    y : np.ndarray [shape=(n,) or (n, c)]
        Audio time series, either single or multichannel

    sr : int > 0
        sampling rate of y

    **kwargs
        keyword arguments to rubberband

    Returns
    -------
    y_mod : np.ndarray [shape=(n,) or (n, c)]
        `y` after rubberband transformation

    '''

    assert sr > 0

    # Get the input and output tempfile
    fd, infile = tempfile.mkstemp(suffix='.wav')
    os.close(fd)
    fd, outfile = tempfile.mkstemp(suffix='.wav')
    os.close(fd)

    # dump the audio
    sf.write(infile, y, sr)

    try:
        # Execute rubberband
        arguments = [__RUBBERBAND_UTIL, '-q']

        for key, value in six.iteritems(kwargs):
            arguments.append(str(key))
            arguments.append(str(value))

        arguments.extend([infile, outfile])

        subprocess.check_call(arguments, stdout=DEVNULL, stderr=DEVNULL)

        # Load the processed audio.
        y_out, _ = sf.read(outfile, always_2d=True)

        # make sure that output dimensions matches input
        if y.ndim == 1:
            y_out = np.squeeze(y_out)

    except OSError as exc:
        six.raise_from(RuntimeError('Failed to execute rubberband. '
                                    'Please verify that rubberband-cli '
                                    'is installed.'),
                       exc)

    finally:
        # Remove temp files
        os.unlink(infile)
        os.unlink(outfile)

    return y_out


def time_stretch(y, sr, rate, rbargs=None):
    '''Apply a time stretch of `rate` to an audio time series.

    This uses the `tempo` form for rubberband, so the
    higher the rate, the faster the playback.


    Parameters
    ----------
    y : np.ndarray [shape=(n,) or (n, c)]
        Audio time series, either single or multichannel

    sr : int > 0
        Sampling rate of `y`

    rate : float > 0
        Desired playback rate.

    rbargs
        Additional keyword parameters for rubberband

        See `rubberband -h` for details.

    Returns
    -------
    y_stretch : np.ndarray
        Time-stretched audio

    Raises
    ------
    ValueError
        if `rate <= 0`
    '''

    if rate <= 0:
        raise ValueError('rate must be strictly positive')

    if rate == 1.0:
        return y

    if rbargs is None:
        rbargs = dict()

    rbargs.setdefault('--tempo', rate)

    return __rubberband(y, sr, **rbargs)


def timemap_stretch(y, sr, time_map, rbargs=None):
    '''Apply a timemap stretch to an audio time series.

    This uses the `time` and `timemap` form for rubberband.


    Parameters
    ----------
    y : np.ndarray [shape=(n,) or (n, c)]
        Audio time series, either single or multichannel

    sr : int > 0
        Sampling rate of `y`

    time_map : list
        Each element is a tuple `t` of length 2 which correspond to the input
         frame and desired output frame.
        If t[1] < t[0] the track will be sped up in this area.
        time_map[-1] must correspond to the lengths of the input audio and
         output audio.

    rbargs
        Additional keyword parameters for rubberband

        See `rubberband -h` for details.

    Returns
    -------
    y_stretch : np.ndarray
        Time-stretched audio

    Raises
    ------
    ValueError
        if `rate <= 0`
    '''

    if rbargs is None:
        rbargs = dict()

    time_stretch = time_map[-1][1]/time_map[-1][0]

    rbargs.setdefault('--time', time_stretch)

    fs, stretch_file_name = tempfile.mkstemp(suffix='.txt')
    os.close(fs)

    stretch_file = open(stretch_file_name, 'w')
    for t in time_map:
        stretch_file.write("%d %d\n" % (t[0], t[1]))
    stretch_file.close()

    rbargs.setdefault('--timemap', stretch_file_name)

    y_stretch = __rubberband(y, sr, **rbargs)
    os.unlink(stretch_file_name)

    return y_stretch


def pitch_shift(y, sr, n_steps, rbargs=None):
    '''Apply a pitch shift to an audio time series.

    Parameters
    ----------
    y : np.ndarray [shape=(n,) or (n, c)]
        Audio time series, either single or multichannel

    sr : int > 0
        Sampling rate of `y`

    n_steps : float
        Shift by `n_steps` semitones.

    rbargs
        Additional keyword parameters for rubberband

        See `rubberband -h` for details.

    Returns
    -------
    y_shift : np.ndarray
        Pitch-shifted audio
    '''

    if n_steps == 0:
        return y

    if rbargs is None:
        rbargs = dict()

    rbargs.setdefault('--pitch', n_steps)

    return __rubberband(y, sr, **rbargs)
