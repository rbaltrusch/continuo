# -*- coding: utf-8 -*-
"""Generator module tests"""

import numpy
import pytest

from music_generation import generator, scale, duration, music_algorithm, layer


def test_generator(monkeypatch):
    layers = layer.init_layers()
    generator_ = generator.Generator(
        scale=scale.Scale("A3", "major"),
        duration=duration.Duration(time_length=1, tempo=120),
        music_generator=music_algorithm.MusicGenerator(),
    )

    def make_piece_mock(layers, _, size=4):  # 4 eight notes in one second
        for i in range(size):
            for layer in layers:
                layer.notes.append(i)

    monkeypatch.setattr(music_algorithm, "make_piece", make_piece_mock)
    data = generator_.generate_music(layers)
    assert generator_.duration.eigth == 0.25
    assert isinstance(data, numpy.ndarray)
    assert data.size == 44100
