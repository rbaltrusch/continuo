# -*- coding: utf-8 -*-
"""Scale module tests"""

import pytest
import musical.theory

from continuo import scale


@pytest.mark.parametrize("base,octave,tonality", [("A", 3, "major"), ("B", 2, "minor")])
def test_scale(base, octave, tonality):
    scale_ = scale.Scale(key=f"{base}{octave}", tonality=tonality)
    expected_scale = musical.theory.Scale(
        musical.theory.Note(f"{base}{octave}"), tonality
    )
    assert scale_.scale.__dict__ == expected_scale.__dict__


@pytest.mark.parametrize("length", [2, 5, 7])
def test_notes(length):
    scale_ = scale.Scale("A3", "major", length=length)
    assert scale_.notes == list(range(length))
