# -*- coding: utf-8 -*-
"""Layer module tests"""

from itertools import zip_longest
import pytest

from music_generation import layer


@pytest.mark.parametrize(
    "number_of_layers,layer_offsets",
    [
        (0, (0, 12, 24)),
        (1, (0, 12, 24)),
        (2, (0, 12, 24)),
        (4, []),
        (4, (0, 12)),
    ],
)
def test_init_layers(number_of_layers, layer_offsets):
    layers = layer.init_layers(
        number_of_layers=number_of_layers, layer_offsets=layer_offsets
    )
    assert len(layers) == number_of_layers
    for layer_, offset in zip_longest(layers, layer_offsets, fillvalue=0):
        if layer_ == 0:
            break
        assert layer_.offset == offset


@pytest.mark.parametrize(
    "notes",
    [
        [],
        [1, 2, 3],
    ],
)
def test_layer(notes):
    layer_ = layer.Layer(notes[:])
    assert layer_.notes == notes
    assert notes == list(layer_)
    if notes:
        assert notes[0] == layer_[0]

    new_notes = [2, 3, 4]
    layer_.extend(new_notes)
    assert notes + new_notes == layer_.notes
    assert notes + new_notes == list(layer_)
