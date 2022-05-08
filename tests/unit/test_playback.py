# -*- coding: utf-8 -*-
"""Playback module tests"""

import numpy
from music_generation import playback

def test_playback():
    playback.play(data=numpy.ndarray((1, 2)))
