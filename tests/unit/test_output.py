# -*- coding: utf-8 -*-
"""Output module tests"""

import os

import numpy

from continuo import output, layer


def teardown():
    if os.path.isfile("test.wav"):
        os.unlink("test.wav")

    if os.path.isfile("test.json"):
        os.unlink("test.json")


def test_wav():
    output.save_to_wav_file(data=numpy.ndarray((1, 1)), filepath="test.wav")
    assert os.path.isfile("test.wav")


def test_json():
    layers = layer.init_layers(number_of_layers=3, layer_offsets=(0, 12, 24))
    for layer_ in layers:
        layer_.extend([1, 2, 3])

    filepath = "test.json"
    output.save_to_json(layers, filepath)
    loaded_layers = output.load_from_json(filepath)
    assert layers == loaded_layers
