# pyrubberband
[![PyPI](https://img.shields.io/pypi/v/pyrubberband.svg)](https://pypi.python.org/pypi/pyrubberband)
[![Build Status](https://travis-ci.org/bmcfee/pyrubberband.svg)](https://travis-ci.org/bmcfee/pyrubberband)
[![Coverage Status](https://coveralls.io/repos/bmcfee/pyrubberband/badge.svg?branch=testing&service=github)](https://coveralls.io/github/bmcfee/pyrubberband?branch=testing)
[![GitHub license](https://img.shields.io/github/license/bmcfee/pyrubberband.svg)]()
[![Documentation Status](https://readthedocs.org/projects/pyrubberband/badge/?version=latest)](http://pyrubberband.readthedocs.org/en/latest/?badge=latest)

A python wrapper for [rubberband](http://breakfastquay.com/rubberband/).

For now, this just provides lightweight wrappers for pitch-shifting and time-stretching.

All processing is done via the command-line through files on disk.  In the future, this could be improved
by directly wrapping the C library instead.

Install Rubberband on OS X
--------------------------

```
brew install https://gist.githubusercontent.com/faroit/b67c1708cdc1f9c4ddc9/raw/942bbedded22f05abab0d09b52383e7be4aee237/rubberband.rb
```

Example usage
-------------

```python

>>> import soundfile as sf
>>> import pyrubberband as pyrb
>>> # Read mono wav file
>>> y, sr = sf.read("test.wav")
>>> # Play back at double speed
>>> y_stretch = pyrb.time_stretch(y, sr, 2.0)
```
