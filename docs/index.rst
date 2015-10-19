.. pyrubberband documentation master file, created by
   sphinx-quickstart on Mon Oct 19 10:40:20 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyRubberband
============

A python wrapper for `rubberband <http://breakfastquay.com/rubberband/>`_.

For now, this just provides lightweight wrappers for pitch-shifting and time-stretching.

All processing is done via the command-line through files on disk.  In the future, this could be improved
by directly wrapping the C library instead.

Example usage
-------------
.. code-block:: python

    >>> import librosa
    >>> import pyrubberband as pyrb
    >>> y, sr = librosa.load(librosa.util.example_audio_file())
    >>> # Play back at double speed
    >>> y_stretch = pyrb.time_stretch(y, sr, 2.0)
    >>> # Play back two semi-tones higher
    >>> y_shift = pyrb.pitch_shift(y, sr, 2)
    

API Reference
-------------
.. toctree::
    :maxdepth: 3
    
    api

Contribute
----------
- `Issue Tracker <http://github.com/bmcfee/pyrubberband/issues>`_
- `Source Code <http://github.com/bmcfee/pyrubberband>`_
