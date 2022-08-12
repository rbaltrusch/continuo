# -*- coding: utf-8 -*-
"""Duration module tests"""

import math

import pytest

from continuo import duration


@pytest.mark.parametrize(
    "time_length,tempo,motif_length",
    [(10, 120, 10), (15, 65, 15), (0, 120, 10), (10, 120, 1)],
)
def test_duration(time_length, tempo, motif_length):
    duration_ = duration.Duration(
        time_length=time_length, tempo=tempo, motif_length=motif_length
    )
    assert math.isclose(duration_.eigth, 30 / tempo, rel_tol=0.05)
    assert math.isclose(
        duration_.length, math.ceil(time_length * tempo / (30 * motif_length))
    )
