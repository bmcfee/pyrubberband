# pyrubberband
[![Build Status](https://travis-ci.org/bmcfee/pyrubberband.svg)](https://travis-ci.org/bmcfee/pyrubberband)
[![Coverage Status](https://coveralls.io/repos/bmcfee/pyrubberband/badge.svg?branch=testing&service=github)](https://coveralls.io/github/bmcfee/pyrubberband?branch=testing)
[![GitHub license](https://img.shields.io/github/license/bmcfee/pyrubberband.svg)]()
[![Documentation Status](https://readthedocs.org/projects/pyrubberband/badge/?version=latest)](http://pyrubberband.readthedocs.org/en/latest/?badge=latest)

A python wrapper for [rubberband](http://breakfastquay.com/rubberband/).

For now, this just provides lightweight wrappers for pitch-shifting and time-stretching.

All processing is done via the command-line through files on disk.  In the future, this could be improved
by directly wrapping the C library instead.

Example usage
-------------

```python

>>> import librosa
>>> import pyrubberband as pyrb
>>> y, sr = librosa.load(librosa.util.example_audio_file())
>>> # Play back at double speed
>>> y_stretch = pyrb.time_stretch(y, sr, 2.0)
```
