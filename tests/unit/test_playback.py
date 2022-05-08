# -*- coding: utf-8 -*-
"""Playback module tests"""

import numpy
import pytest
from music_generation import playback

@pytest.mark.skip_workflow
def test_playback():
    playback.play(data=numpy.ndarray((1, 2)))
