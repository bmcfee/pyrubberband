#!/usr/bin/env python
# CREATED:2015-03-02 11:36:15 by Brian McFee <brian.mcfee@nyu.edu>
'''Command-line wrapper for rubberband

.. autosummary::
    :toctree: generated/

    pitch_shift
    time_stretch
    timemap_stretch
    ableton_asd_to_time_map
'''


import os
import subprocess
import tempfile
import six
import numpy as np
import soundfile as sf


__all__ = ['time_stretch', 'pitch_shift', 'timemap_stretch', 'ableton_asd_to_time_map']

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
        y_out, _ = sf.read(outfile, always_2d=True, dtype=y.dtype)

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

    A timemap stretch allows non-linear time-stretching by mapping source to
    target sample frame numbers for fixed time points within the audio data.

    This uses the `time` and `timemap` form for rubberband.

    Parameters
    ----------
    y : np.ndarray [shape=(n,) or (n, c)]
        Audio time series, either single or multichannel

    sr : int > 0
        Sampling rate of `y`

    time_map : list
        Each element is a tuple `t` of length 2 which corresponds to the
        source sample position and target sample position.

        If `t[1] < t[0]` the track will be sped up in this area.

        `time_map[-1]` must correspond to the lengths of the source audio and
        target audio.

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
        if `time_map` is not monotonic
        if `time_map` is not non-negative
        if `time_map[-1][0]` is not the input audio length
    '''

    if rbargs is None:
        rbargs = dict()

    is_positive = all(time_map[i][0] >= 0 and time_map[i][1] >= 0
                      for i in range(len(time_map)))
    is_monotonic = all(time_map[i][0] <= time_map[i+1][0] and
                       time_map[i][1] <= time_map[i+1][1]
                       for i in range(len(time_map)-1))
    if not is_positive:
        raise ValueError('time_map should be non-negative')

    if not is_monotonic:
        raise ValueError('time_map is not monotonic')

    if time_map[-1][0] != len(y):
        raise ValueError('time_map[-1] should correspond to the last sample')

    time_stretch = time_map[-1][1] * 1.0 / time_map[-1][0]
    rbargs.setdefault('--time', time_stretch)

    stretch_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt',
                                               delete=False)
    try:
        for t in time_map:
            stretch_file.write('{:0} {:1}\n'.format(t[0], t[1]))
        stretch_file.close()

        rbargs.setdefault('--timemap', stretch_file.name)
        y_stretch = __rubberband(y, sr, **rbargs)
    finally:
        # Remove temp file
        os.unlink(stretch_file.name)

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

def ableton_asd_to_time_map(filepath, y, sr, bpm):

    '''Parse an Ableton `asd` file into a time map to be used with `timemap_stretch`.

    Parameters
    ----------
    filepath : str
        Path to an Ableton warp file with ".asd" extension 

    y : np.ndarray [shape=(n,) or (n, c)]
        Audio time series, either single or multichannel

    sr : int > 0
        Sampling rate of `y`

    bpm : float > 0
        The beats-per-minute of the time map which will be returned

    Returns
    -------
    time_map : list
        Each element is a tuple `t` of length 2 which corresponds to the
        source sample position and target sample position.

        If `t[1] < t[0]` the track will be sped up in this area.

        Refer to the function `timemap_stretch`.
    '''

    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"No such file or directory: '{filepath}'")

    f = open(filepath, 'rb')
    asd_bin = f.read()
    f.close()

    index = asd_bin.find(b'SampleOverViewLevel')
    index = asd_bin.find(b'SampleOverViewLevel', index+1)
    index += 90

    # a double is 8 bytes
    size_double = 8

    import struct
    def read_double(buffer, index):
        return struct.unpack('d', buffer[index:index+size_double])[0]

    def read_bool(buffer, index):
        return struct.unpack('?', buffer[index:index+1])[0]

    loop_start = read_double(asd_bin, index)
    index += size_double
    loop_end = read_double(asd_bin, index)
    index += size_double
    sample_offset = read_double(asd_bin, index)
    index += size_double
    hidden_loop_start = read_double(asd_bin, index)
    index += size_double
    hidden_loop_end = read_double(asd_bin, index)
    index += size_double
    end_marker = read_double(asd_bin, index)
    index += size_double

    start_marker = loop_start + sample_offset

    # These values are measured in quarter notes relative to the 1.1.1 marker.
    # loop_start, loop_end, hidden_loop_start, hidden_loop_end, start_marker, end_marker

    warp_markers = []
    index = asd_bin.find(b'WarpMarker')
    last_good_index = -1
    while True:

        index = asd_bin.find(b'WarpMarker', index+1)
        if index < 0:
            index = last_good_index
            break

        index += 14  # WarpMarker is 10 bytes. Then add 4.

        marker_seconds = read_double(asd_bin, index)
        index += size_double
        marker_beats = read_double(asd_bin, index)

        warp_markers.append((marker_beats, marker_seconds))

        last_good_index = index

    index += 15
    # The loop_on value can be found some bytes after the last warp marker.
    loop_on = read_bool(asd_bin, index)

    time_map = []
    for marker_beats, marker_seconds in warp_markers:
        
        time_map.append([int(marker_seconds*sr), int(marker_beats*(60./bpm)*sr)])

    # The difference in beats divided by the difference in seconds, times 60 seconds = BPM.
    last_bpm = (warp_markers[-1][0] - warp_markers[-2][0]) / (warp_markers[-1][1] - warp_markers[-2][1]) * 60.

    num_samples = y.shape[1] if len(y.shape) > 1 else y.shape[0]

    # Extrapolate the last bpm 
    mapped_last_sample = time_map[-1][1] + (num_samples-time_map[-1][0])*last_bpm/bpm

    time_map.append([num_samples, mapped_last_sample])

    return time_map
