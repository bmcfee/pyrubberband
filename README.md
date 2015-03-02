# pyrubberband
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
