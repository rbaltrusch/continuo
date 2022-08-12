# -*- coding: utf-8 -*-
"""Music algorithm module tests"""

import continuo
import pytest

from continuo import music_algorithm, layer


def test_get_consonance():
    music_generator = music_algorithm.MusicGenerator()
    for i in range(14):
        expected_value = music_generator.consonance_dict.get(i % 7)
        assert music_generator.get_consonance(0, i) == expected_value


def test_get_most_consonant_motif():
    music_generator = music_algorithm.MusicGenerator(
        consonance_dict={0: 1, 1: 2, 2: 0, 3: 0.5, 4: 0.5, 5: 0.5}
    )

    layers = [
        layer.Layer(notes=[0, 1, 2]),
        layer.Layer(notes=[2, 2, 4]),
    ]

    motifs = [
        [0, 2, 4],
        [1, 2, 3],
        [4, 5, 7],
    ]

    chosen_motif = music_generator.get_most_consonant_motif(motifs, layers)
    assert chosen_motif == [1, 2, 3]


@pytest.mark.parametrize(
    "motif, expected",
    [
        ([], 0),
        ([1, 2, 3], 4),
    ],
)
def test_get_motif_consonance(motif, expected):
    music_generator = music_algorithm.MusicGenerator(
        consonance_dict={0: 1, 1: 2, 2: 4, 3: 6}
    )
    layers = [layer.Layer(notes=[0, 0, 0])]
    consonance = music_generator.get_motif_consonance(motif, layers)
    assert consonance == expected


@pytest.mark.parametrize(
    "motif_length, expected_length, expected_values",
    [
        (0, 0, []),
        (20, 20, [0] * 19 + [4]),
    ],
)
def test_make_progression(motif_length, expected_length, expected_values):
    music_generator = music_algorithm.MusicGenerator(
        harmony_dict={k: [0] for k in range(7)}, motif_length=motif_length
    )
    progression = music_generator.make_progression()
    assert len(progression) == expected_length
    assert progression == expected_values


def test_make_motif():
    music_generator = music_algorithm.MusicGenerator(motif_length=5)
    layers = layer.init_layers(number_of_layers=3)
    for layer_ in layers:
        layer_.extend(range(8))

    motif = music_generator.make_motif(layers)
    assert all(isinstance(x, int) for x in motif)
    assert len(motif) == music_generator.motif_length


def test_smooth_bassline():
    bass_lines = [[1, 1, 2, 1], [1, 2, 3, 2], [2, 2, 4, 2]]
    chosen_bass_line = music_algorithm.smooth_bass_line(bass_lines)
    assert chosen_bass_line == [1, 1, 2, 1]


def test_create_variations():
    variations = music_algorithm.create_variations(bass_line=[0], num=1)
    assert variations[0] in [[0], [2], [4]]


def test_make_piece(monkeypatch):
    music_generator = music_algorithm.MusicGenerator(
        harmony_dict={k: [0] for k in range(7)}, motif_length=5
    )

    layers = layer.init_layers(number_of_layers=3)

    music_generator.make_motif = lambda *_, **__: [1] * music_generator.motif_length
    monkeypatch.setattr(music_algorithm, "create_variations", lambda x, num=1: [x])
    music_algorithm.make_piece(layers, music_generator)
    print(music_generator.harmony_dict)
    assert list(layers[0]) == [0] * 4 + [4]
    assert list(layers[1]) == [1] * 5
    assert list(layers[2]) == [1] * 5


def test_make_piece_empty():
    music_generator = music_algorithm.MusicGenerator()
    music_algorithm.make_piece(layers=[], music_generator=music_generator)
