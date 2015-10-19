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

import librosa


__all__ = ['time_stretch', 'pitch_shift']


def __rubberband(y, sr, **kwargs):
    '''Execute rubberband

    Parameters
    ----------
    y : np.ndarray [shape=(n,) or (2, n)]
        Audio time series, either mono or stereo

    sr : int > 0
        sampling rate of y

    **kwargs
        keyword arguments to rubberband

    Returns
    -------
    y_mod : np.ndarray
        `y` after rubberband transformation

    '''

    assert sr > 0

    # Get the input and output tempfile
    fd, infile = tempfile.mkstemp(suffix='.wav')
    os.close(fd)
    fd, outfile = tempfile.mkstemp(suffix='.wav')
    os.close(fd)

    # dump the audio
    librosa.output.write_wav(infile, y, sr)

    try:
        # Execute rubberband
        arguments = ['rubberband', '-q']

        for key, value in six.iteritems(kwargs):
            arguments.append(str(key))
            arguments.append(str(value))

        arguments.extend([infile, outfile])

        subprocess.check_call(arguments)

        # Load the processed audio.
        # Setting mono=False will ensure that the shape matches `y`
        y_out, _ = librosa.load(outfile, sr=sr, mono=False)

    finally:
        # Remove temp files
        os.unlink(infile)
        os.unlink(outfile)
        pass

    return y_out


def time_stretch(y, sr, rate, rbargs=None):
    '''Apply a time stretch of `rate` to an audio time series.

    This uses the `tempo` form for rubberband, so the
    higher the rate, the faster the playback.


    Parameters
    ----------
    y : np.ndarray [shape=(n,) or (2, n)]
        Audio time series, either mono or stereo

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


def pitch_shift(y, sr, n_steps, rbargs=None):
    '''Apply a pitch shift to an audio time series.

    Parameters
    ----------
    y : np.ndarray [shape=(n,) or (2, n)]
        Audio time series, either mono or stereo

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
