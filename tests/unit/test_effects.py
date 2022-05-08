# -*- coding: utf-8 -*-
"""Effects module tests"""

import numpy
from music_generation import effects

def test_effects():
    effects.apply_effects(numpy.ndarray((1, 1)))
