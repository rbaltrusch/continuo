# -*- coding: utf-8 -*-
"""Config module tests"""

import json
import os

import pytest

from music_generation import config, music_algorithm


def teardown():
    if os.path.isfile("test_config.json"):
        os.unlink("test_config.json")


def test_happy_path():
    filepath = "test_config.json"
    old_generator = music_algorithm.MusicGenerator()
    config.write_configuration_file(filepath, old_generator)
    contents = config.read_configuration_file(
        filepath,
        required_fields=["momentums", "intervals", "consonance_dict", "harmony_dict"],
    )

    dict_ = {k: tuple(v) if isinstance(v, list) else v for k, v in contents.items()}
    new_generator = music_algorithm.MusicGenerator(**dict_)
    assert new_generator == old_generator


def test_required_missing():
    with open("test_config.json", "w") as file:
        json.dump({}, file)

    with pytest.raises(config.ConfigurationError):
        config.read_configuration_file(
            "test_config.json", required_fields=["something"]
        )
